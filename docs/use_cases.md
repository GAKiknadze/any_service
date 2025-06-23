# Use Cases

## Auth

### Login

`auth.LoginUseCase`

### Registration

Not implemented

`composite.user.RegistrationUseCase`:
- `auth.RegisterUseCase`
- `profile.CreateUseCase`

### Verify

Not implemented

### Change password

Not implemented

### Refresh tokens

`auth.RefreshTokenUseCase`

### Authorize by access token

`auth.AuthorizeUseCase`

### Logout

`auth.LogoutUseCase`

---

## Sessions

### Get sessions list

`auth.GetSessionsUseCase`

### Delete session by id

`auth.DeleteSessionUseCase`

---

## Profile

### Get user public info by id

Not implemented

`profile.GetUserPublicInfoUseCase`

### Get user private info by id

Not implemented

`composite.user.GetUserPrivateInfoUseCase`:
- `auth.GetAuthUserUseCase`
- `profile.GetUserInfoUseCase`

### Search user public info by id

`profile.SearchUserInfoByNickNameUseCase`

### Update user info

`profile.UpdateUserInfoUseCase`

### Change email

Not implemented

### Change password

Not implemented
