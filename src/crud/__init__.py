import pydantic.main
from pydantic.fields import ModelField, ForwardRef
from pydantic import BaseModel
from .exceptions import *
from .user.models import (
    UserPublic,
    UserPrivate,
    UserAuthorizationForm,
    UserRegistrationForm,
    UserShared,
    UserPublicWithGroups,
)
from .subscription.models import (
    SubscriptionInfo,
    SubscriptionVariant,
    SubscriptionVariantFull,
)
from .group.models import (
    Group,
    GroupMember,
    GroupHistoryEntry,
    GroupWithHistory,
    GroupFull,
    GroupMemberShared,
)
from .attachments import *
deps = {
    'UserPublic': UserPublic,
    'list[UserPublic]': list[UserPublic],
    'UserShared': UserShared,
    'list[UserShared]': list[UserShared],
    'list[GroupFull]': list[GroupFull],
    'GroupFull': GroupFull,
}
kdeps = list(deps.keys())
ls = list(locals().values())
for i in ls:
    if type(i) != pydantic.main.ModelMetaclass:
        continue
    i.update_forward_refs(**deps)


from .user import *
from .friends import *
from .attachments.models import *
from .group import *

