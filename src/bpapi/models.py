from decimal import Decimal
from typing import List
from typing_extensions import Annotated
from sqlalchemy import (
    ForeignKey,
    Integer,
    Table,
    Column,
    DECIMAL,
)
from sqlalchemy.orm import (
    relationship,
    DeclarativeBase,
    Mapped,
    mapped_column,
    # MappedAsDataclass,  # causes infinite recursion
)


class Base(DeclarativeBase):
    pass


id_pk = Annotated[int, mapped_column('id', Integer, primary_key=True)]
rowid_pk = Annotated[int, mapped_column('rowid', Integer, primary_key=True)]
partnum_fk = Annotated[int, mapped_column(ForeignKey('partnum.rowid'))]

partnumber_junction = Table(
    'refers',
    Base.metadata,
    Column('predecessor', Integer, ForeignKey('partnum.rowid'), primary_key=True),
    Column('successor', Integer, ForeignKey('partnum.rowid'), primary_key=True),
)


class Section(Base):
    """
    Section of Bosch catalogue hierarchy.
    """
    __tablename__ = 'sect'

    id: Mapped[id_pk]
    title: Mapped[str]
    # subsections: Mapped[list['SubSection']] = relationship(back_populates='section')


class SubSection(Base):
    """
    Subsection of Bosch catalogue hierarchy. Refers to Section.
    """
    __tablename__ = 'subsect'

    id: Mapped[id_pk]
    title: Mapped[str]
    sect_id: Mapped[int] = mapped_column(ForeignKey('sect.id'))
    # section: Mapped['Section'] = relationship(lazy='joined')
    # subsubsections: Mapped[list['Subsub']] = relationship(back_populates='subsection')


class Subsub(Base):
    """
    Subsubsection of Bosch catalogue heirarchy. Refers to Subsection.
    """
    __tablename__ = 'subsub'

    id: Mapped[rowid_pk]
    title: Mapped[str]
    subsect_id: Mapped[int] = mapped_column(ForeignKey('subsect.id'))
    # subsection: Mapped['SubSection'] = relationship(back_populates='subsubsections')
    subsub_products: Mapped[list['Product']] = relationship(back_populates='subsub')


class PartNumber(Base):
    """
    partnum table entry. Represents every patnum occured in Bosch price, whether
    in price itself or in new release, discontinued or reference sections.
    Stored along with flags - discontinued or new release. And refers to self
    to bound similar products.
    """
    __tablename__ = 'partnum'

    id: Mapped[rowid_pk]
    part_no: Mapped[str]
    discontinued: Mapped[bool]
    new_release: Mapped[bool]
    product: Mapped['Product'] = relationship()
    masterdata: Mapped['MasterData'] = relationship()
    refers: Mapped[list['PartNumber']] = relationship(secondary=partnumber_junction,
                                                      primaryjoin='PartNumber.id == refers.c.predecessor',
                                                      secondaryjoin='PartNumber.id == refers.c.successor',)
    # refers: Mapped[list['PartnumReference']] = relationship(foreign_keys='PartnumReference.predecessor',
    #                                                         lazy='joined')

# class PartnumReference(Base):
#     """
#     Partnum self joining table.
#     """
#     __tablename__ = 'refers'
#
#     id: Mapped[rowid_pk]
#     predecessor: Mapped[int] = mapped_column(ForeignKey('partnum.rowid'))
#     successor: Mapped[int] = mapped_column(ForeignKey('partnum.rowid'))
#     refer: Mapped['PartNumber'] = relationship(foreign_keys='PartnumReference.successor',
#                                                lazy='joined')


class Product(Base):
    """
    Bosch product in pricelist. Stores descriptions, references on sections, price
    and some product related parameters. References on particular partnum entry.
    """
    __tablename__ = 'pricelist'

    title_ua: Mapped[str]
    title_en: Mapped[str]
    uktzed: Mapped[int]
    min_order: Mapped[int]
    quantity: Mapped[int]
    price: Mapped[str]
    truck: Mapped[bool]
    id: Mapped[rowid_pk]
    partnum_id: Mapped[partnum_fk]
    # partnum: Mapped['PartNumber'] = relationship(back_populates='product')
    subsub_id: Mapped[int] = mapped_column(ForeignKey('subsub.rowid'))
    subsub = relationship('Subsub')


class MasterData(Base):
    """
    Physical pararmeters of product. Weigth, dimensions, etc.
    """
    __tablename__ = 'masterdata'

    ean: Mapped[int]
    gross: Mapped[str]
    net: Mapped[str]
    weight_unit: Mapped[str]
    length: Mapped[int]
    width: Mapped[int]
    height: Mapped[int]
    measure_unit: Mapped[str]
    volume: Mapped[str]
    volume_unit: Mapped[str]
    id: Mapped[rowid_pk]
    partnum_id: Mapped[partnum_fk]
    # partnum: Mapped['PartNumber'] = relationship(back_populates='masterdata')
