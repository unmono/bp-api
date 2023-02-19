from decimal import Decimal
from typing import List
from typing_extensions import Annotated
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import (
    relationship,
    DeclarativeBase,
    Mapped,
    mapped_column,
    MappedAsDataclass,
)


class Base(DeclarativeBase, MappedAsDataclass):
    pass


id_pk = Annotated[int, mapped_column('id', Integer, init=False, primary_key=True)]
rowid_pk = Annotated[int, mapped_column('rowid', Integer, init=False, primary_key=True)]
partnum_fk = Annotated[int, mapped_column(ForeignKey('partnum.id'))]


class PartnumReference(Base):
    """
    Partnum self joining table.
    """
    __tablename__ = 'refers'

    id: Mapped[rowid_pk]
    predecessor: Mapped[int] = mapped_column(ForeignKey('partnum.id'))
    successor: Mapped[int] = mapped_column(ForeignKey('partnum.id'))


class Section(Base):
    """
    Section of Bosch catalogue hierarchy.
    """
    __tablename__ = 'sect'

    id: Mapped[id_pk]
    title: Mapped[str]
    subsections: Mapped[List['SubSection']] = relationship(back_populates='section')


class SubSection(Base):
    """
    Subsection of Bosch catalogue hierarchy. Refers to Section.
    """
    __tablename__ = 'subsect'

    id: Mapped[id_pk]
    title: Mapped[str]
    sect_id: Mapped[int] = mapped_column(ForeignKey('sect.id'))
    section: Mapped['Section'] = relationship(back_populates='subsections')
    subsubsections: Mapped['Subsub'] = relationship(back_populates='subsection')


class Subsub(Base):
    """
    Subsubsection of Bosch catalogue heirarchy. Refers to Subsection.
    """
    __tablename__ = 'subsub'

    id: Mapped[id_pk]
    title: Mapped[str]
    subsect_id: Mapped[int] = mapped_column(ForeignKey('subsect.id'))
    subsubsections: Mapped['SubSection'] = relationship(back_populates='subsubsection')


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
    products: Mapped['Product'] = relationship(back_populates='partnumber')  # Same name as field? Without name?
    masterdata: Mapped['MasterData'] = relationship(back_populates='partnumber')
    refers: Mapped[List['PartnumReference']] = relationship()


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
    price: Mapped[Decimal]
    truck: Mapped[bool]
    id: Mapped[rowid_pk]
    partnum_id: Mapped[partnum_fk]
    partnum: Mapped['PartNumber'] = relationship()
    subsub_id: Mapped[int] = mapped_column(ForeignKey('subsub.id'))
    subsub: Mapped['PartNumber'] = relationship(back_populates='products')


class MasterData(Base):
    """
    Physical pararmeters of product. Weigth, dimensions, etc.
    """
    __tablename__ = 'masterdata'

    ean: Mapped[int]
    gross: Mapped[Decimal]
    net: Mapped[Decimal]
    weight_unit: Mapped[str]
    length: Mapped[int]
    width: Mapped[int]
    height: Mapped[int]
    measure_unit: Mapped[str]
    volume: Mapped[Decimal]
    volume_unit: Mapped[str]
    id: Mapped[rowid_pk]
    partnum_id: Mapped[partnum_fk]
    partnum: Mapped['PartNumber'] = relationship(back_populates='masterdata')
