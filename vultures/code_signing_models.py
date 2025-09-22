from sqlalchemy import Column, String, Integer, LargeBinary, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from base import UUIDBase, User
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from datetime import datetime

# Could be an optional AST section
type Code = Str # | Binary | LargeBinary | AST # Work on this later!

# This could facilliate novel machine generated code
# Use signers_uuid to look up their public key
# Link to pki database
class Object(UUIDBase):
    __tablename__ = "class_objects"
    
    signer: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.uuid"), nullable=True) 
    code: Mapped[Code] = mapped_column(Code, nullable=False)
    
# It's possible to have the ast objects and the script reviewed and signed by separate parties
## Ex: anonymous platform provider signs their object/ast... which is integrated by the contracting (host) company
class Script(UUIDBase):
    __tablename__ = "scripts"
    
    name: Mapped[str] = mapped_column(String(256), nullable=False)    
    required_objects: Mapped[List[UUID]] = mapped_column(PGUUID(as_uuid=True), ForeignKey("object.uuid"), default=[])
    required_libraries: Mapped["Library"] = mapped_column(Library, ForeignKey("library.uuid"), nullable=True)
    script_raw: Mapped[Code] = mapped_column(Code, nullable=False)
    # script_embeddings: Mapped[Any]
    
    signers: Mapped[List[UUID]] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.uuid"), default=[])
    
# A library is a module
class Library(UUIDBase):
    __tablename__ = "library"
    
    name: Mapped[str]
    version: Mapped[Tuple[int, int, int]]
    scripts: Mapped[List["Script"]] = mapped_column(Script, ForeignKey("scripts.uuid"), nullable=False)
    # config_files: Mapped[Any]
    
    signers: Mapped[List[UUID]] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.uuid"), default=[])
    
# No required packages as this is bad form... that would be a namespace!
class Package(UUIDBase):
    __tablename__ = "package"
    
    required_libraries: Mapped["Library"] = mapped_column(Library, ForeignKey("library.uuid"), nullable=True)
    is_namespace: Mapped[Bool] = mapped_column(Bool, default=False)
    required_packages: Mapped["Package"] = mapped_column(PGUUID(as_uuid=True), ForeignKey("package.uuid"), default=[])
    repo_url: Mapped[Str] = mapped_column(String(256), nullable=True)
    # config_files: Mapped[Any
    
if __name__ == "__main__":
    Base.metadata.create_all(engine)
