"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# OTIKA specific schemas

class Lead(BaseModel):
    """
    Leads generated from the contact form
    Collection: "lead"
    """
    full_name: str = Field(..., min_length=2, description="Client full name")
    email: EmailStr = Field(..., description="Client email")
    company: Optional[str] = Field(None, description="Company or organization")
    phone: Optional[str] = Field(None, description="Phone number")
    budget_range: Optional[str] = Field(None, description="Estimated budget range")
    message: Optional[str] = Field(None, description="Project description / needs")
    interests: List[str] = Field(default_factory=list, description="Services of interest")
    source: Optional[str] = Field(None, description="How they found us")

class Project(BaseModel):
    """
    Portfolio projects
    Collection: "project"
    """
    title: str = Field(..., description="Project title")
    slug: str = Field(..., description="URL slug")
    client: Optional[str] = Field(None, description="Client name")
    category: str = Field(..., description="Category e.g. landing, ecommerce, saas, mobile, branding")
    description: Optional[str] = Field(None, description="Short description")
    cover_image: Optional[str] = Field(None, description="Cover image URL")
    tags: List[str] = Field(default_factory=list, description="Tags")
    case_url: Optional[str] = Field(None, description="Link to live site or case study")

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
