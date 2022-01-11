from enum import IntEnum, Enum


class ProcurementListStatus(IntEnum):
    Draft = 10
    AwaitingForApproval = 20
    Rejected = 30
    Approved = 40
    Ordered = 50

    @classmethod
    def choices(cls, key=None):
        DATA_MAP = (
            (10, 'Draft'),
            (20, 'Awaiting for Approval'),
            (30, 'Rejected'),
            (40, 'Approved'),
            (50, 'Ordered'),
        )
        return DATA_MAP if key is None else dict(DATA_MAP).get(key, 'UNKNOWN')


print(ProcurementListStatus.get_choices())
