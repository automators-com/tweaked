tmp_schema = """from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    DateTime,
    Boolean,
    ForeignKey,
    Enum,
    ARRAY,
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
import enum

Base = declarative_base()


class ProjectRoles(enum.Enum):
    SalesManager = "SalesManager"
    DeliveryManager = "DeliveryManager"


class AppRoles(enum.Enum):
    owner = "owner"
    admin = "admin"
    user = "user"


class Capacity(Base):
    __tablename__ = "Capacity"

    id = Column(
        String,
        primary_key=True,
        default=func.uuid_generate_v4(),
        info={"provider": "uuid4"},
    )
    created_at = Column(DateTime, default=func.now(), info={"provider": "date"})
    units = Column(Float, info={"provider": "random_number"})
    month = Column(DateTime, info={"provider": "date"})
    locked = Column(Integer, info={"provider": "random_number"})

    project_id = Column(String, ForeignKey("Project.id", ondelete="CASCADE"))
    Project = relationship("Project", back_populates="Capacity")
    rate_id = Column(String, ForeignKey("Rate.id", ondelete="CASCADE"))
    Rate = relationship("Rate", back_populates="Capacity")


class Client(Base):
    __tablename__ = "Client"

    id = Column(
        String,
        primary_key=True,
        default=func.uuid_generate_v4(),
        info={"provider": "uuid4"},
    )
    name = Column(String, info={"provider": "company"})
    street = Column(String, info={"provider": "street_address"})
    country = Column(String, info={"provider": "country"})
    city = Column(String, info={"provider": "city"})
    tax_number = Column(String, nullable=True, info={"provider": "ssn"})
    tax = Column(Float, nullable=True, info={"provider": "random_number"})
    currency = Column(String, default="EUR", info={"provider": "currency_code"})
    postcode = Column(Integer, info={"provider": "postcode"})
    payment_term = Column(Integer, default=14, info={"provider": "random_number"})
    working_hours = Column(
        Float, default=8, nullable=True, info={"provider": "random_number"}
    )

    clientId = Column(String, ForeignKey("Client.id"), nullable=True)
    PartnerClient = relationship("Client", remote_side=[id], backref="PartnerClients")

    org_id = Column(String, ForeignKey("Organization.id", ondelete="CASCADE"))
    Organization = relationship("Organization", back_populates="Client")
    Project = relationship("Project", back_populates="Client")


class Invoice(Base):
    __tablename__ = "Invoice"

    id = Column(
        String,
        primary_key=True,
        default=func.uuid_generate_v4(),
        info={"provider": "uuid4"},
    )
    invoice_date = Column(DateTime, default=func.now(), info={"provider": "date"})
    time_period = Column(String, nullable=True, info={"provider": "date"})
    invoice_number = Column(String, unique=True, info={"provider": "uuid4"})
    total_amount = Column(Float, info={"provider": "random_number"})
    discount = Column(Float, nullable=True, info={"provider": "random_number"})
    description = Column(String, nullable=True, info={"provider": "sentence"})
    country = Column(String, nullable=True, info={"provider": "country"})
    due_date = Column(DateTime, nullable=True, info={"provider": "date"})
    reference = Column(String, nullable=True, info={"provider": "random_number"})
    payment_note = Column(String, nullable=True, info={"provider": "sentence"})
    client_id = Column(String, nullable=True, info={"provider": "uuid4"})
    client_name = Column(String, nullable=True, info={"provider": "company"})
    client_street = Column(String, nullable=True, info={"provider": "street_address"})
    client_country = Column(String, nullable=True, info={"provider": "country"})
    client_city = Column(String, nullable=True, info={"provider": "city"})
    client_tax = Column(Float, nullable=True, info={"provider": "random_number"})
    client_tax_number = Column(String, nullable=True, info={"provider": "ssn"})
    client_due_date = Column(DateTime, nullable=True, info={"provider": "date"})
    client_postcode = Column(Integer, nullable=True, info={"provider": "postcode"})
    client_partner_client_id = Column(String, nullable=True, info={"provider": "uuid4"})

    org_id = Column(String, ForeignKey("Organization.id", ondelete="CASCADE"))
    Organization = relationship("Organization", back_populates="Invoice")
    InvoiceLine = relationship("InvoiceLine", back_populates="Invoice")


class InvoiceLine(Base):
    __tablename__ = "InvoiceLine"

    id = Column(
        String,
        primary_key=True,
        default=func.uuid_generate_v4(),
        info={"provider": "uuid4"},
    )
    assigned = Column(String, nullable=True, info={"provider": "uuid4"})
    price = Column(Float, info={"provider": "random_amount"})
    amount = Column(Float, info={"provider": "random_amount"})
    total = Column(ARRAY(Float), info={"provider": "random_double_precision_array"})
    project_name = Column(String, nullable=True, info={"provider": "sentence"})

    project_id = Column(
        String, ForeignKey("Project.id", ondelete="CASCADE"), nullable=True
    )
    Project = relationship("Project", back_populates="InvoiceLine")
    invoice_id = Column(String, ForeignKey("Invoice.id", ondelete="CASCADE"))
    Invoice = relationship("Invoice", back_populates="InvoiceLine")


class User(Base):
    __tablename__ = "User"

    id = Column(
        String,
        primary_key=True,
        default=func.uuid_generate_v4(),
        info={"provider": "uuid4"},
    )
    email = Column(String, unique=True, info={"provider": "email"})
    first_name = Column(String, info={"provider": "first_name"})
    last_name = Column(String, info={"provider": "last_name"})
    password = Column(String, info={"provider": "password"})
    password_reset_code = Column(
        Integer, nullable=True, info={"provider": "random_number"}
    )

    UserOrganization = relationship("UserOrganization", back_populates="User")


class UserOrganization(Base):
    __tablename__ = "UserOrganization"

    id = Column(
        String,
        primary_key=True,
        default=func.uuid_generate_v4(),
        info={"provider": "uuid4"},
    )
    org_id = Column(String, ForeignKey("Organization.id", ondelete="CASCADE"))
    start_date = Column(DateTime, info={"provider": "date"})
    end_date = Column(DateTime, nullable=True, info={"provider": "date"})
    consultancy_percentage = Column(
        Float, default=100, info={"provider": "random_number"}
    )
    relation = Column(String, nullable=True, info={"provider": "sentence"})
    country = Column(String, nullable=True, info={"provider": "country"})
    rate = Column(Float, nullable=True, info={"provider": "random_number"})
    show_in_planning = Column(Boolean, default=True, info={"provider": "boolean"})
    team_lead_id = Column(String, ForeignKey("UserOrganization.id"), nullable=True)
    is_team_lead = Column(Boolean, default=False, info={"provider": "boolean"})
    is_approved = Column(Boolean, default=True, info={"provider": "boolean"})
    role = Column(
        Enum(AppRoles),
        default=AppRoles.user,
        info={"provider": f"enum:{",".join([i.value for i in AppRoles])}"},
    )
    last_login = Column(DateTime, nullable=True, info={"provider": "date"})
    user_id = Column(String, ForeignKey("User.id"))

    TeamLead = relationship("UserOrganization", remote_side=[id], backref="TeamMembers")
    Organization = relationship("Organization", back_populates="UserOrganization")
    ProjectRole = relationship("ProjectRole", back_populates="UserOrganization")
    Time = relationship("Time", back_populates="UserOrganization")
    Rate = relationship("Rate", back_populates="UserOrganization")
    User = relationship("User", back_populates="UserOrganization")


class WorkDay(Base):
    __tablename__ = "WorkDay"

    id = Column(
        String,
        primary_key=True,
        default=func.uuid_generate_v4(),
        info={"provider": "uuid4"},
    )
    month = Column(DateTime, info={"provider": "date"})
    units = Column(Float, info={"provider": "random_number"})
    city = Column(String, info={"provider": "city"})


class Organization(Base):
    __tablename__ = "Organization"

    id = Column(
        String,
        primary_key=True,
        default=func.uuid_generate_v4(),
        info={"provider": "uuid4"},
    )
    name = Column(String, unique=True, info={"provider": "company"})

    Client = relationship("Client", back_populates="Organization")
    UserOrganization = relationship("UserOrganization", back_populates="Organization")
    Invite = relationship("Invite", back_populates="Organization")
    Invoice = relationship("Invoice", back_populates="Organization")


class Time(Base):
    __tablename__ = "Time"

    id = Column(
        String,
        primary_key=True,
        default=func.uuid_generate_v4(),
        info={"provider": "uuid4"},
    )
    note = Column(String, nullable=True, info={"provider": "sentence"})
    duration = Column(String, info={"provider": "time"})
    start_time = Column(DateTime, info={"provider": "date"})
    break_duration = Column(DateTime, nullable=True, info={"provider": "date"})
    locked = Column(Boolean, default=False, info={"provider": "boolean"})
    billable = Column(Boolean, info={"provider": "boolean"})

    project_id = Column(String, ForeignKey("Project.id", ondelete="CASCADE"))
    Project = relationship("Project", back_populates="Time")
    user_org_id = Column(String, ForeignKey("UserOrganization.id", ondelete="CASCADE"))
    UserOrganization = relationship("UserOrganization", back_populates="Time")


class Project(Base):
    __tablename__ = "Project"

    id = Column(
        String,
        primary_key=True,
        default=func.uuid_generate_v4(),
        info={"provider": "uuid4"},
    )
    internal_code = Column(String, unique=True, info={"provider": "uuid4"})
    external_code = Column(String, nullable=True, info={"provider": "uuid4"})
    name = Column(String, info={"provider": "sentence"})
    country = Column(String, nullable=True, info={"provider": "country"})
    start_date = Column(DateTime, info={"provider": "date"})
    end_date = Column(DateTime, nullable=True, info={"provider": "date"})
    billing = Column(String, info={"provider": "sentence"})
    price = Column(Float, info={"provider": "random_number"})
    units_total = Column(Float, info={"provider": "random_number"})
    signed = Column(Boolean, info={"provider": "boolean"})

    client_id = Column(String, ForeignKey("Client.id", ondelete="CASCADE"))
    Client = relationship("Client", back_populates="Project")
    Time = relationship("Time", back_populates="Project")
    Rate = relationship("Rate", back_populates="Project")
    Capacity = relationship("Capacity", back_populates="Project")
    InvoiceLine = relationship("InvoiceLine", back_populates="Project")
    ProjectRole = relationship("ProjectRole", back_populates="Project")


class Rate(Base):
    __tablename__ = "Rate"

    id = Column(
        String,
        primary_key=True,
        default=func.uuid_generate_v4(),
        info={"provider": "uuid4"},
    )
    rate = Column(Float, info={"provider": "random_number"})
    role = Column(
        String,
        nullable=True,
        info={"provider": f"enum:{",".join([i.value for i in ProjectRoles])})"},
    )
    hours = Column(Float, nullable=True, info={"provider": "random_number"})

    user_org_id = Column(String, ForeignKey("UserOrganization.id", ondelete="CASCADE"))
    UserOrganization = relationship("UserOrganization", back_populates="Rate")
    project_id = Column(String, ForeignKey("Project.id", ondelete="CASCADE"))
    Project = relationship("Project", back_populates="Rate")
    Capacity = relationship("Capacity", back_populates="Rate")


class Invite(Base):
    __tablename__ = "Invite"

    id = Column(
        String,
        primary_key=True,
        default=func.uuid_generate_v4(),
        info={"provider": "uuid4"},
    )
    email = Column(String, unique=True, info={"provider": "email"})
    first_name = Column(String, info={"provider": "first_name"})
    last_name = Column(String, info={"provider": "last_name"})
    start_date = Column(DateTime, info={"provider": "date"})
    end_date = Column(DateTime, nullable=True, info={"provider": "date"})
    consultancy_percentage = Column(
        Float, default=100, info={"provider": "random_number"}
    )
    relation = Column(String, nullable=True, info={"provider": "sentence"})
    country = Column(String, info={"provider": "country"})
    rate = Column(Float, nullable=True, info={"provider": "random_number"})
    show_in_planning = Column(Boolean, default=True, info={"provider": "boolean"})
    team_lead_id = Column(String, info={"provider": "uuid4"})

"""
