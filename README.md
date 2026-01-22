# DiveIn 🌊

DiveIn is a secure, modern, and user-friendly CLI tool for managing and connecting to your SSH hosts. It serves as a robust alternative to managing a complex `~/.ssh/config` file, offering features like encrypted password storage and an interactive interface.

## Features

-   **Secure Storage**: SSH passwords are encrypted using AES (Fernet) with a master password.
-   **Interactive UI**: Beautiful terminal interface powered by `Rich` and `Typer`.
-   **Quick Connect**: Connect to hosts by ID (`divein 1`) or nickname (`divein my-server`).
-   **Bulk Management**: Delete multiple hosts at once with range support (`divein rm 1-3,5`).
-   **Native Experience**: Seamless SSH integration without external dependencies like `sshpass`.

## Installation

Clone the repository and install it locally:

```bash
git clone https://github.com/yourusername/divein.git
cd divein
pip install -e .
```

## Usage

### Add a Host
Add a new SSH host. You will be prompted for a Master Password to encrypt your SSH password.

```bash
divein add
```

### List Hosts
View all your managed hosts in a table. You can interactively connect or delete hosts from this view.

```bash
divein list
```

### Connect
Connect to a host directly using its ID or nickname.

```bash
divein 1
# or
divein production-server
```

### View Details
See detailed information about a specific host.

```bash
divein show 1
```

### Remove Hosts
Delete hosts by ID, nickname, or range.

```bash
divein rm 1
divein rm 2-5,old-server
```

## Security

DiveIn uses PBKDF2HMAC for key derivation and Fernet (AES) for symmetric encryption. Your Master Password is used to unlock your SSH credentials only when needed and is never stored on disk.
