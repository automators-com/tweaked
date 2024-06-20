import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ARRAY


Base = declarative_base()


class Capacity(Base):

    __tablename__ = 'Capacity'

    id = sa.Column(sa.Text(), nullable=False)
    created_at = sa.Column(sa.TIMESTAMP(3), nullable=False, server_default=func.now())
    units = sa.Column(double precision(), nullable=False)
    locked = sa.Column(sa.Integer(), nullable=False)
    project_id = sa.Column(sa.Text(), nullable=False)
    user_org_id = sa.Column(sa.Text(), nullable=False)
    month = sa.Column(sa.TIMESTAMP(3), nullable=False)


class Client(Base):

    __tablename__ = 'Client'

    id = sa.Column(sa.Text(), nullable=False)
    name = sa.Column(sa.Text(), nullable=False)
    street = sa.Column(sa.Text(), nullable=False)
    country = sa.Column(sa.Text(), nullable=False)
    city = sa.Column(sa.Text(), nullable=False)
    tax_number = sa.Column(sa.Text())
    postcode = sa.Column(sa.Integer(), nullable=False)
    org_id = sa.Column(sa.Text(), nullable=False)
    payment_term = sa.Column(sa.Integer(), nullable=False, server_default='14')
    client_id = sa.Column(sa.Text())
    currency = sa.Column(sa.Text(), nullable=False, server_default='EUR' ::text)
    tax = sa.Column(double precision())
    working_hours = sa.Column(double precision(), server_default='8')


class Invite(Base):

    __tablename__ = 'Invite'

    id = sa.Column(sa.Text(), nullable=False)
    email = sa.Column(sa.Text(), nullable=False)
    first_name = sa.Column(sa.Text(), nullable=False)
    last_name = sa.Column(sa.Text(), nullable=False)
    start_date = sa.Column(sa.TIMESTAMP(3), nullable=False)
    end_date = sa.Column(sa.TIMESTAMP(3))
    consultancy_percentage = sa.Column(double precision(), nullable=False, server_default='100')
    relation = sa.Column(sa.Text())
    country = sa.Column(sa.Text(), nullable=False)
    rate = sa.Column(double precision())
    show_in_planning = sa.Column(sa.Boolean(), nullable=False, server_default='true')
    team_lead_id = sa.Column(sa.Text())
    is_team_lead = sa.Column(sa.Boolean(), nullable=False, server_default='false')
    role = sa.Column(sa.Text(), nullable=False, server_default='user' ::text)
    expiry = sa.Column(sa.TIMESTAMP(3), nullable=False)
    invite_accepted = sa.Column(sa.Boolean(), nullable=False, server_default='false')
    created_at = sa.Column(sa.TIMESTAMP(3), nullable=False, server_default=func.now())
    org_id = sa.Column(sa.Text(), nullable=False)


class Invoice(Base):

    __tablename__ = 'Invoice'

    id = sa.Column(sa.Text(), nullable=False)
    invoice_date = sa.Column(sa.TIMESTAMP(3), nullable=False, server_default=func.now())
    time_period = sa.Column(sa.Text())
    invoice_number = sa.Column(sa.Text(), nullable=False)
    total_amount = sa.Column(double precision(), nullable=False)
    discount = sa.Column(double precision())
    description = sa.Column(sa.Text())
    country = sa.Column(sa.Text())
    due_date = sa.Column(sa.TIMESTAMP(3))
    reference = sa.Column(sa.Text())
    client_id = sa.Column(sa.Text())
    client_name = sa.Column(sa.Text())
    client_street = sa.Column(sa.Text())
    client_country = sa.Column(sa.Text())
    client_city = sa.Column(sa.Text())
    client_tax_number = sa.Column(sa.Text())
    client_due_date = sa.Column(sa.TIMESTAMP(3))
    client_postcode = sa.Column(sa.Integer())
    client_partner_client_id = sa.Column(sa.Text())
    org_id = sa.Column(sa.Text(), nullable=False)
    client_tax = sa.Column(double precision())
    payment_note = sa.Column(sa.Text())


class InvoiceLine(Base):

    __tablename__ = 'InvoiceLine'

    id = sa.Column(sa.Text(), nullable=False)
    assigned = sa.Column(sa.Text())
    price = sa.Column(double precision(), nullable=False)
    amount = sa.Column(double precision(), nullable=False)
    total = sa.Column(ARRAY(double precision()))
    project_id = sa.Column(sa.Text())
    invoice_id = sa.Column(sa.Text(), nullable=False)
    project_name = sa.Column(sa.Text())


class Organization(Base):

    __tablename__ = 'Organization'

    id = sa.Column(sa.Text(), nullable=False)
    name = sa.Column(sa.Text(), nullable=False)


class Project(Base):

    __tablename__ = 'Project'

    id = sa.Column(sa.Text(), nullable=False)
    external_code = sa.Column(sa.Text())
    name = sa.Column(sa.Text(), nullable=False)
    country = sa.Column(sa.Text())
    start_date = sa.Column(sa.TIMESTAMP(3), nullable=False)
    end_date = sa.Column(sa.TIMESTAMP(3))
    billing = sa.Column(sa.Text(), nullable=False)
    price = sa.Column(double precision(), nullable=False)
    units_total = sa.Column(double precision(), nullable=False)
    signed = sa.Column(sa.Boolean(), nullable=False)
    client_id = sa.Column(sa.Text(), nullable=False)
    internal_code = sa.Column(sa.Text(), nullable=False)


class Rate(Base):

    __tablename__ = 'Rate'

    id = sa.Column(sa.Text())
    rate = sa.Column(double precision())
    role = sa.Column(sa.Text())
    hours = sa.Column(double precision())
    user_org_id = sa.Column(sa.Text())
    project_id = sa.Column(sa.Text())


class Time(Base):

    __tablename__ = 'Time'

    id = sa.Column(sa.Text(), nullable=False)
    note = sa.Column(sa.Text())
    duration = sa.Column(sa.Text(), nullable=False)
    start_time = sa.Column(sa.TIMESTAMP(3), nullable=False)
    break_duration = sa.Column(sa.TIMESTAMP(3))
    locked = sa.Column(sa.Boolean(), nullable=False, server_default='false')
    billable = sa.Column(sa.Boolean(), nullable=False)
    project_id = sa.Column(sa.Text(), nullable=False)
    user_org_id = sa.Column(sa.Text(), nullable=False)


class User(Base):

    __tablename__ = 'User'

    id = sa.Column(sa.Text(), nullable=False)
    email = sa.Column(sa.Text(), nullable=False)
    first_name = sa.Column(sa.Text(), nullable=False)
    last_name = sa.Column(sa.Text(), nullable=False)
    password = sa.Column(sa.Text(), nullable=False)
    password_reset_code = sa.Column(sa.Integer())


class WorkDay(Base):

    __tablename__ = 'WorkDay'

    id = sa.Column(sa.Text(), nullable=False)
    month = sa.Column(sa.TIMESTAMP(3), nullable=False)
    units = sa.Column(double precision(), nullable=False)
    city = sa.Column(sa.Text(), nullable=False)


class PrismaMigrations(Base):

    __tablename__ = '_prisma_migrations'

    id = sa.Column(sa.String(36), nullable=False)
    checksum = sa.Column(sa.String(64), nullable=False)
    finished_at = sa.Column(sa.TIMESTAMP())
    migration_name = sa.Column(sa.String(255), nullable=False)
    logs = sa.Column(sa.Text())
    rolled_back_at = sa.Column(sa.TIMESTAMP())
    started_at = sa.Column(sa.TIMESTAMP(), nullable=False, server_default=func.now())
    applied_steps_count = sa.Column(sa.Integer(), nullable=False, server_default='0')


class TempTable(Base):

    __tablename__ = 'temp_table'

    id = sa.Column(sa.Text())
    external_code = sa.Column(sa.Text())
    name = sa.Column(sa.Text())
    country = sa.Column(sa.Text())
    start_date = sa.Column(sa.TIMESTAMP())
    end_date = sa.Column(sa.TIMESTAMP())
    billing = sa.Column(sa.Text())
    price = sa.Column(double precision())
    units_total = sa.Column(double precision())
    signed = sa.Column(sa.Boolean())
    client_id = sa.Column(sa.Text())
    internal_code = sa.Column(sa.Text())


class Tmp(Base):

    __tablename__ = 'tmp'

    id = sa.Column(sa.Text())
    external_code = sa.Column(sa.Text())
    name = sa.Column(sa.Text())
    country = sa.Column(sa.Text())
    start_date = sa.Column(sa.TIMESTAMP())
    end_date = sa.Column(sa.TIMESTAMP())
    billing = sa.Column(sa.Text())
    price = sa.Column(double precision())
    units_total = sa.Column(double precision())
    signed = sa.Column(sa.Boolean())
    client_id = sa.Column(sa.Text())
    internal_code = sa.Column(sa.Text())
