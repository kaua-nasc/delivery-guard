from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from ...models.user import User
from ...database.session import get_db
from ...core.security import get_password_hash, verify_password
from ...core.auth import get_current_active_user
from ...schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
    UserStatusUpdate,
    UserPasswordUpdate
)

router = APIRouter()

@router.post("/users/", 
             response_model=UserResponse,
             status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Somente admin pode criar usuários
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can create new users"
        )

    # Verifica se username ou email já existem
    existing_user = await db.execute(
        select(User).filter(
            (User.username == user.username) | 
            (User.email == user.email)
        )
    )
    existing_user = existing_user.scalars().first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

    # Cria o usuário
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=get_password_hash(user.password),
        full_name=user.full_name,
        role=user.role.value
    )
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user

@router.get("/users/", response_model=List[UserResponse])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Somente admin pode listar todos usuários
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can list all users"
        )

    result = await db.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Usuário pode ver seu próprio perfil ou admin pode ver qualquer perfil
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own profile"
        )

    user = await db.execute(select(User).filter(User.id == user_id))
    user = user.scalars().first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Somente admin ou o próprio usuário pode atualizar
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own profile"
        )

    # Busca o usuário
    result = await db.execute(select(User).filter(User.id == user_id))
    db_user = result.scalars().first()
    
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Atualiza os campos
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "role" and current_user.role != "admin":
            continue  # Somente admin pode mudar roles
        setattr(db_user, field, value)

    db_user.updated_at = func.now()
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user

@router.patch("/users/{user_id}/status", response_model=UserResponse)
async def update_user_status(
    user_id: int,
    status_update: UserStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Somente admin pode alterar status de usuários
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can change user status"
        )

    # Não permite desativar a si mesmo
    if current_user.id == user_id and not status_update.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot deactivate yourself"
        )

    result = await db.execute(select(User).filter(User.id == user_id))
    db_user = result.scalars().first()
    
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db_user.is_active = status_update.is_active
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user

@router.put("/users/{user_id}/password", response_model=UserResponse)
async def update_user_password(
    user_id: int,
    password_update: UserPasswordUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Somente o próprio usuário pode mudar sua senha
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only change your own password"
        )

    result = await db.execute(select(User).filter(User.id == user_id))
    db_user = result.scalars().first()
    
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Verifica a senha atual
    if not verify_password(password_update.current_password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    # Atualiza a senha
    db_user.password_hash = get_password_hash(password_update.new_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Somente admin pode deletar usuários
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can delete users"
        )

    # Não permite deletar a si mesmo
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot delete yourself"
        )

    result = await db.execute(select(User).filter(User.id == user_id))
    db_user = result.scalars().first()
    
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    await db.delete(db_user)
    await db.commit()
    
    return None