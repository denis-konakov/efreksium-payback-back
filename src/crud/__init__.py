from .user.models import UserPublic, UserPrivate, UserAuthorizationData, UserRegistrationData
from .subscription.models import Subscription, SubscriptionVariant
from .group.models import Group, GroupMember, GroupHistoryEntry
deps = {
    'UserPublic': UserPublic,
}
Subscription.update_forward_refs(**deps)
GroupMember.update_forward_refs(**deps)
GroupHistoryEntry.update_forward_refs(**deps)
