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
-- username
    'Иван Иванов',
-- email
    'user@example.com',
-- number
    '+79999999999',
-- hashed_password
    '$2b$12$jnF03F1OnOlydXejKFZJfOYz2Ga.KNSeRk3urC60aillm2BeTMuHO', -- string
-- email_confirmed
    TRUE,
-- avatar
    'DEFAULT'
)