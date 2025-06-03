from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())
    
    devs = relationship('Dev', secondary='freebies', backref='companies')

    def __repr__(self):
        return f'<Company {self.name}>'
    @classmethod
    def oldest_company(cls):
       return session.query(cls).order_by(cls.founding_year).first()
        
   

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    def received_one(self, item_name):
     return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, dev, freebie):
      if freebie.dev == self:
        freebie.dev = dev
        session.commit()

    
class Freebie(Base):
    __tablename__ ="freebies"

    id = Column(Integer(), primary_key=True)
    item_name=Column(String())
    value=Column(Integer())

    dev_id = Column(Integer(), ForeignKey('devs.id'))
    company_id = Column(Integer(), ForeignKey('companies.id'))
    
    dev = relationship('Dev', backref='freebies')
    company = relationship('Company', backref='freebies')

    

    
    def print_details(self):
     return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"
    
    # def give_freebie(self, dev, item_name, value):
    # freebie = Freebie(
    #     item_name=item_name,
    #     value=value,
    #     company_id=self.id,
    #     dev_id=dev.id
    # )
    # session.add(freebie)
    # session.commit()
    
    
   


