INSERT INTO
    users
(
    "username",
    "email",
    "number",
    "hashed_password",
    "email_confirmed",
    "avatar"
)
values (
    'Иван Иванов',
    'user@example.com',
    '+79999999999',
    '$2b$12$jnF03F1OnOlydXejKFZJfOYz2Ga.KNSeRk3urC60aillm2BeTMuHO', -- string
    TRUE,
    'DEFAULT'
)