"""

**OMEGA global variables.**

Runtime options and database connection variables to be populated during initialization.

----

**CODE**

"""


print('importing %s' % __file__)

# globals to be populated at runtime:
options = None  #: simulation options
engine = None  #: connection to database engine
session = None  #: database session
pass_num = 0  #: multi-pass pass number
producer_shares_mode = False  #: producer shares mode when True
manufacturer_aggregation = False  #: true if manufacturer-level detail in vehicle aggregation
price_modification_data = None  #: holds price modification data for the current compliance_id and calendar year
locked_price_modification_data = None  #: holds price locked modification data for the current compliance_id and calendar year
