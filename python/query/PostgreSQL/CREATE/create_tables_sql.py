create_Booking = """
DROP TABLE IF EXISTS public.Booking;

CREATE TABLE IF NOT EXISTS public.Booking (
    BookingID BIGINT NOT NULL PRIMARY KEY,
    BookingParentID BIGINT,
    Status SMALLINT,
    RecordLocator CHAR(6),
    BookingPromoCode VARCHAR(8),
    CurrencyCode CHAR(3),
    HoldDateTime VARCHAR(32),
    ExpiredDate TIMESTAMP,
    PriceStatus SMALLINT,
    PaidStatus SMALLINT,
    SystemCode CHAR(3),
    ChannelType VARCHAR(32),
    CreatedAgentCode VARCHAR(32),
    CreatedOrganizationCode VARCHAR(32),
    CreatedDomainCode CHAR(3),
    CreatedLocationCode CHAR(5),
    SourceAgentCode VARCHAR(32),
    SourceOrganizationCode VARCHAR(32),
    SourceDomainCode CHAR(5),
    SourceLocationCode CHAR(5),
    ReferralCode VARCHAR(32),
    GroupName VARCHAR(64),
    ReceivedBy VARCHAR(64),
    ReceivedByReference VARCHAR(32),
    ProfileStatus SMALLINT,
    PaxResidentCountry CHAR(2),
    CreatedSystemType SMALLINT,
    BookingDate TIMESTAMP,
    BookingType CHAR(3),
    OwningCarrierCode CHAR(3),
    CreatedAgentID BIGINT,
    CreatedDate TIMESTAMP,
    ModifiedAgentID BIGINT,
    ModifiedDate TIMESTAMP,
    extract_dt TIMESTAMP,
    source VARCHAR(32),
    proc_status VARCHAR(32),
    TimeToModify INTERVAL,
    business_key VARCHAR(50),
    hash VARCHAR(50)
);

"""

create_BookingNew = """
DROP TABLE IF EXISTS public.BookingNew;

CREATE TABLE IF NOT EXISTS public.BookingNew (
    BookingID BIGINT NOT NULL PRIMARY KEY,
    BookingParentID BIGINT,
    Status SMALLINT,
    RecordLocator CHAR(6),
    BookingPromoCode VARCHAR(8),
    CurrencyCode CHAR(3),
    HoldDateTime VARCHAR(32),
    ExpiredDate TIMESTAMP,
    PriceStatus SMALLINT,
    PaidStatus SMALLINT,
    SystemCode CHAR(3),
    ChannelType VARCHAR(32),
    CreatedAgentCode VARCHAR(32),
    CreatedOrganizationCode VARCHAR(32),
    CreatedDomainCode CHAR(3),
    CreatedLocationCode CHAR(5),
    SourceAgentCode VARCHAR(32),
    SourceOrganizationCode VARCHAR(32),
    SourceDomainCode CHAR(5),
    SourceLocationCode CHAR(5),
    ReferralCode VARCHAR(32),
    GroupName VARCHAR(64),
    ReceivedBy VARCHAR(64),
    ReceivedByReference VARCHAR(32),
    ProfileStatus SMALLINT,
    PaxResidentCountry CHAR(3),
    CreatedSystemType SMALLINT,
    BookingDate TIMESTAMP,
    BookingType CHAR(3),
    OwningCarrierCode CHAR(3),
    CreatedAgentID BIGINT,
    CreatedDate TIMESTAMP,
    ModifiedAgentID BIGINT,
    ModifiedDate TIMESTAMP,
    extract_dt TIMESTAMP,
    source VARCHAR(32),
    proc_status VARCHAR(32),
    TimeToModify INTERVAL,
    business_key VARCHAR(50),
    hash VARCHAR(50)
);

"""
create_BookingPassenger = """ 
DROP TABLE IF EXISTS public.BookingPassenger;
CREATE TABLE IF NOT EXISTS public.BookingPassenger (
    PassengerID BIGINT NOT NULL PRIMARY KEY,
    DOB VARCHAR(10),
    PaxType CHAR(4),
    Gender SMALLINT,
    WeightCategory SMALLINT,
    Suffix CHAR(6),
    BookingSearchNameID BIGINT,
    Nationality CHAR(4),
    ResidentCountry CHAR(4),
    DiscountCode CHAR(4),
    Infant SMALLINT,
    PseudoPassenger BOOLEAN,
    BookingID BIGINT,
    CustomerNumber VARCHAR(32),
    ProgramCode CHAR(4),
    ProgramLevel VARCHAR(32),
    ProgramNumber VARCHAR(32),
    FamilyNumber SMALLINT,
    TotalCost MONEY,
    BalanceDue MONEY,
    CreatedAgentID BIGINT,
    CreatedDate TIMESTAMP,
    ModifiedAgentID BIGINT,
    ModifiedDate TIMESTAMP,
    extract_dt TIMESTAMP,
    source VARCHAR(32),
    proc_status VARCHAR(32),
    age DECIMAL,
    IsAdult BOOLEAN,
    TimeToModify INTERVAL,
    business_key VARCHAR(50),
    hash VARCHAR(50)
);
"""

create_BookingPassengerNew = """ 
DROP TABLE IF EXISTS public.BookingPassengerNew;
CREATE TABLE IF NOT EXISTS public.BookingPassengerNew (
    PassengerID BIGINT NOT NULL PRIMARY KEY,
    DOB VARCHAR(10),
    PaxType CHAR(4),
    Gender SMALLINT,
    WeightCategory SMALLINT,
    Suffix CHAR(6),
    BookingSearchNameID BIGINT,
    Nationality CHAR(4),
    ResidentCountry CHAR(4),
    DiscountCode CHAR(4),
    Infant SMALLINT,
    PseudoPassenger SMALLINT,
    BookingID BIGINT,
    CustomerNumber VARCHAR(32),
    ProgramCode CHAR(4),
    ProgramLevel VARCHAR(32),
    ProgramNumber VARCHAR(32),
    FamilyNumber SMALLINT,
    TotalCost MONEY,
    BalanceDue MONEY,
    CreatedAgentID BIGINT,
    CreatedDate TIMESTAMP,
    ModifiedAgentID BIGINT,
    ModifiedDate TIMESTAMP,
    extract_dt TIMESTAMP,
    source VARCHAR(32),
    proc_status VARCHAR(32),
    age DECIMAL,
    IsAdult BOOLEAN,
    TimeToModify INTERVAL,
    business_key VARCHAR(50),
    hash VARCHAR(50)
);

"""


create_PassengerJourneyCharge = """
DROP TABLE IF EXISTS public.PassengerJourneyCharge;
CREATE TABLE IF NOT EXISTS public.PassengerJourneyCharge (
    PassengerID BIGINT NOT NULL,
    SegmentID BIGINT NOT NULL,
    ChargeNumber SMALLINT NOT NULL,
    ChargeType SMALLINT,
    ChargeCode CHAR(6),
    TicketCode CHAR(3),
    CurrencyCode CHAR(3),
    ChargeAmount MONEY,
    ChargeDetail VARCHAR(32),
    ForeignCurrencyCode CHAR(3),
    ForeignAmount MONEY,
    CreatedAgentID BIGINT,
    CreatedDate TIMESTAMP,
    extract_dt TIMESTAMP,
    source VARCHAR(32),
    proc_status VARCHAR(32),
    PassengerJourneyCharge VARCHAR(32),
    business_key VARCHAR(50),
    hash VARCHAR(50),
    PRIMARY KEY (PassengerID, SegmentID, ChargeNumber)
);
"""

create_PassengerJourneyLeg = """
DROP TABLE IF EXISTS public.PassengerJourneyLeg;
CREATE TABLE IF NOT EXISTS public.PassengerJourneyLeg (
    PassengerID BIGINT NOT NULL,
    SegmentID BIGINT NOT NULL,
    LegNumber SMALLINT NOT NULL,
    InventoryLegID BIGINT,
    DepartureDetail VARCHAR(32),
    ArrivalDetail VARCHAR(32),
    JourneyNumber SMALLINT,
    BookingStatus CHAR(2),
    SeatPreference CHAR(3),
    SeatTogetherPreference SMALLINT,
    CompartmentDesignator CHAR(4),
    UnitDesignator VARCHAR(6),
    UnitAssignmentWeight INTEGER,
    BoardingSequence SMALLINT,
    LiftStatus SMALLINT,
    PriorityCode VARCHAR(32),
    PriorityDate VARCHAR(32),
    CreatedAgentID BIGINT,
    CreatedDate TIMESTAMP,
    ModifiedAgentID BIGINT,
    ModifiedDate TIMESTAMP,
    extract_dt TIMESTAMP,
    source VARCHAR(32),
    proc_status VARCHAR(32),
    TimeToModify INTERVAL,
    business_key VARCHAR(50),
    hash VARCHAR(50),
    PRIMARY KEY (PassengerID, SegmentID, LegNumber)
);

"""

create_PassengerJourneySegment = """
DROP TABLE IF EXISTS public.PassengerJourneySegment;
CREATE TABLE IF NOT EXISTS public.PassengerJourneySegment (
    PassengerID BIGINT NOT NULL,
    SegmentID BIGINT NOT NULL,
    DepartureDate DATE,
    DepartureStation CHAR(3),
    ArrivalStation CHAR(3),
    TripType SMALLINT,
    TripNumber SMALLINT,
    JourneyNumber SMALLINT,
    SegmentNumber SMALLINT,
    FareComponentNumber SMALLINT,
    FareJourneyType SMALLINT,
    BookingStatus CHAR(2),
    ClassOfService VARCHAR(32),
    TravelClassCode VARCHAR(32),
    ClassType VARCHAR(32),
    International SMALLINT,
    GoverningFare SMALLINT,
    FlexibleFare SMALLINT,
    VerifiedTravelDocs VARCHAR(44),
    FareStatus SMALLINT,
    FareClassOfService VARCHAR(32),
    ProductClassCode CHAR(4),
    CurrencyCode CHAR(3),
    RuleTariff DECIMAL(10, 2),
    RuleCarrierCode CHAR(3),
    RuleNumber CHAR(4),
    FareBasis VARCHAR(32),
    FareDiscountCode VARCHAR(32),
    TicketNumber DECIMAL,
    InfantTicketNumber DECIMAL,
    TicketIndicator CHAR(3),
    TicketStatus VARCHAR(32),
    OverbookIndicator VARCHAR(32),
    ChangeReasonCode VARCHAR(32),
    SegmentType VARCHAR(32),
    XRefCarrierCode VARCHAR(32),
    XRefFlightNumber DECIMAL,
    XRefOpSuffix VARCHAR(32),
    XRefClassOfService VARCHAR(32),
    ChannelType VARCHAR(32),
    CreatedAgentCode VARCHAR(32),
    CreatedOrganizationCode VARCHAR(32),
    CreatedDomainCode CHAR(3),
    CreatedLocationCode CHAR(5),
    SourceAgentCode VARCHAR(16),
    SourceOrganizationCode VARCHAR(32),
    SourceDomainCode CHAR(5),
    SourceLocationCode CHAR(5),
    SalesDate TIMESTAMP,
    ActivityDate TIMESTAMP,
    CreatedAgentID BIGINT,
    CreatedDate TIMESTAMP,
    ModifiedAgentID BIGINT,
    ModifiedDate TIMESTAMP,
    extract_dt TIMESTAMP,
    source VARCHAR(32),
    proc_status VARCHAR(32),
    TimeToModify INTERVAL,
    business_key VARCHAR(50),
    hash VARCHAR(50),
    PRIMARY KEY (PassengerID, SegmentID)
);
"""