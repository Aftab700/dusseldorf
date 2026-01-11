import argparse
import asyncio
import re
import sys
from pathlib import Path

from tabulate import tabulate

# Resolve path for local imports
script_dir = Path(__file__).resolve().parent
sys.path.append(str(script_dir))

from config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient
from services.auth_helper import get_password_hash

# --- Constants and Validation Logic ---
ALLOWED_ROLES = {"readonly", "readwrite", "assignroles", "owner", "admin"}
# Allows: a-z, A-Z, 0-9, dot (.), and underscore (_)
USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9._]+$")


def validate_user_input(username: str, roles: list = None):
    """Enforces strict character sets for usernames and whitelisted roles."""
    if not USERNAME_REGEX.match(username):
        print(f"ERROR: Invalid username '{username}'.")
        print(
            "Usernames may only contain alphanumeric characters, dots (.), and underscores (_)."
        )
        sys.exit(1)

    if roles:
        invalid_roles = [r for r in roles if r.lower() not in ALLOWED_ROLES]
        if invalid_roles:
            print(f"ERROR: Invalid roles detected: {invalid_roles}")
            print(f"Permitted roles are: {', '.join(sorted(ALLOWED_ROLES))}")
            sys.exit(1)


# --- Database and Operations ---


async def get_db():
    settings = get_settings()
    client = AsyncIOMotorClient(settings.DSSLDRF_CONNSTR)
    return client.get_default_database()


async def list_users():
    db = await get_db()
    users = await db.users.find({}, {"hashed_password": 0}).to_list(None)

    if not users:
        print("No users found in the database.")
        return

    table_data = [
        [u.get("username"), u.get("full_name"), ", ".join(u.get("roles", []))]
        for u in users
    ]
    print("\n--- Registered Users ---")
    print(
        tabulate(
            table_data, headers=["Username", "Full Name", "Roles"], tablefmt="grid"
        )
    )
    print(f"Total: {len(users)}\n")


async def delete_user(username: str):
    # Security Check: Ensure valid format before attempting DB deletion
    validate_user_input(username)

    db = await get_db()

    # User Confirmation
    confirm = input(f"Are you sure you want to delete user '{username}'? (y/N): ")
    if confirm.lower() != "y":
        print("Action cancelled.")
        return

    result = await db.users.delete_one({"username": username})

    if result.deleted_count > 0:
        print(f"Successfully deleted user: {username}")
        await db.sessions.delete_many({"username": username})
    else:
        print(f"Error: User '{username}' not found.")


async def create_or_update_user(username, password, name, roles):
    # Normalize roles to lowercase and validate input
    roles = [r.lower() for r in roles]
    validate_user_input(username, roles)

    db = await get_db()
    hashed_pw = get_password_hash(password)
    user_data = {
        "username": username,
        "hashed_password": hashed_pw,
        "full_name": name,
        "email": username,
        "roles": roles,
    }

    exists = await db.users.find_one({"username": username})
    if exists:
        print(f"User '{username}' already exists. Updating...")
        await db.users.update_one({"username": username}, {"$set": user_data})
    else:
        await db.users.insert_one(user_data)
        print(f"Successfully created user: {username}")


# --- CLI Boilerplate ---


def main():
    settings = get_settings()
    if not settings.DSSLDRF_CONNSTR:
        print("Error: DSSLDRF_CONNSTR not found in .env file.")
        return

    parser = argparse.ArgumentParser(description="User Management CLI for Dusseldorf")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    subparsers.add_parser("list", help="List all users")

    del_parser = subparsers.add_parser("delete", help="Delete a user")
    del_parser.add_argument(
        "-u", "--username", required=True, help="Username to delete"
    )

    create_parser = subparsers.add_parser("upsert", help="Create or Update a user")
    create_parser.add_argument("-u", "--username", required=True)
    create_parser.add_argument("-p", "--password", required=True)
    create_parser.add_argument("-n", "--name", default="User")
    create_parser.add_argument(
        "-r",
        "--roles",
        nargs="+",
        default=["owner"],
        help="Roles: readonly, readwrite, assignroles, owner, admin",
    )

    args = parser.parse_args()

    if args.command == "list":
        asyncio.run(list_users())
    elif args.command == "delete":
        asyncio.run(delete_user(args.username))
    elif args.command == "upsert":
        asyncio.run(
            create_or_update_user(args.username, args.password, args.name, args.roles)
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
