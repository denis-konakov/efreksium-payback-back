from .user.models import UserPublic, UserPrivate, UserAuthorizationData, UserRegistrationData
from .subscription.models import SubscriptionInfo, SubscriptionVariant, SubscriptionVariantFull
from .group.models import Group, GroupMember, GroupHistoryEntry
deps = {
    'UserPublic': UserPublic,
    'list[UserPublic]': list[UserPublic],
}
SubscriptionVariantFull.update_forward_refs(**deps)
SubscriptionInfo.update_forward_refs(**deps)
GroupMember.update_forward_refs(**deps)
GroupHistoryEntry.update_forward_refs(**deps)

from .user import *
