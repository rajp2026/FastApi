ROLE_PERMISSION_MAP = {
    "admin": "*",  # means all permissions
    "user": [
        "product:create",
        "product:read",
    ],
}