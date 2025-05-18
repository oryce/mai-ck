from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Query, HTTPException, status, Response

from .schemas import DocumentDto, TaskIdResponse, PaginatedDocumentsResponse

from app.db.models import DocumentModel, DocumentTagModel, UserModel, DocumentTypeModel

from app.db import db

from peewee import fn, IntegrityError

router = APIRouter(tags=["Работа с документами"])


@router.get(
    "/documents",
    response_model=PaginatedDocumentsResponse,
    summary="Получить документы с фильтрацией и сортировкой",
)
async def get_documents(
    page: int = Query(1, ge=1, description="Номер страницы"),
    per_page: int = Query(10, ge=1, le=100, alias="perPage", description="Документов на странице"),
    sort: str = Query(
        "newest-first", 
        regex="^(newest-first|oldest-first)$",
        description="Сортировка: newest-first или oldest-first"
    ),
    tags: Optional[str] = Query(None, description="Фильтр по тегам (через запятую)"),
):
    try:
        query = DocumentModel.select(
            DocumentModel, 
            UserModel,
            DocumentTypeModel
        ).join(UserModel).switch(DocumentModel).join(DocumentTypeModel)
        
        if tags:
            try:
                tag_ids = list(map(int, tags.split(',')))
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Некорректный формат тегов"
                )
            
            subquery = (
                DocumentTagModel
                .select(DocumentTagModel.document)
                .where(DocumentTagModel.tag_id.in_(tag_ids))
                .group_by(DocumentTagModel.document)
                .having(fn.COUNT(DocumentTagModel.tag_id.distinct()) == len(tag_ids))
            )
            
            query = query.where(DocumentModel.id.in_(subquery))

        order_by = DocumentModel.upload_date.desc() if sort == "newest-first" else DocumentModel.upload_date.asc()
        query = query.order_by(order_by)

        total = query.count()
        per_page = min(per_page, 100)
        pages = (total + per_page - 1) // per_page if total > 0 else 0
        
        if page > pages and pages > 0:
            raise HTTPException(
                status_code=400,
                detail="Некорректный номер страницы"
            )

        documents = query.paginate(page, per_page)

        data = [
            DocumentDto(
                id=doc.id,
                uploaderId=doc.uploader.id,
                name=doc.name,
                uploadDate=doc.upload_date,
                createDate=doc.creation_date,
                typeId=doc.type.id,
            ) for doc in documents
        ]

        return PaginatedDocumentsResponse(
            first=1,
            last=pages if pages > 0 else 0,
            prev=page - 1 if page > 1 else -1,
            next=page + 1 if page < pages else -1,
            pages=pages,
            data=data
        )

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка сервера: {str(e)}"
        )


@router.get(
    "/documents/{document_id}",
    response_model=DocumentDto,
    summary="Получить один документ по id",
)
async def get_document(document_id: int):
    try:
        document = (
            DocumentModel.select(DocumentModel, UserModel, DocumentTypeModel)
            .join(UserModel)
            .switch(DocumentModel)
            .join(DocumentTypeModel)
            .where(DocumentModel.id == document_id)
            .first()
        )
        
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Документ не найден"
            )
            
        return DocumentDto(
            id=document.id,
            uploaderId=document.uploader.id,
            name=document.name,
            uploadDate=document.upload_date,
            createDate=document.creation_date,
            typeId=document.type.id,
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка сервера: {str(e)}"
        )


@router.post(
    "/documents/upload",
    response_model=TaskIdResponse,
    summary="Загрузить документ",
)
async def upload_document(background_tasks: BackgroundTasks): ...


@router.patch(
    "/documents/{document_id}", response_model=DocumentDto, summary="Изменить документ"
)
async def update_document(document_id: int, document: DocumentDto): ...


@router.delete(
    "/documents/{document_id}", 
    summary="Удалить документ",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_document(document_id: int):
    try:
        with db.atomic() as transaction:
            DocumentTagModel.delete().where(
                DocumentTagModel.document == document_id
            ).execute()
            
            deleted_count = DocumentModel.delete().where(
                DocumentModel.id == document_id
            ).execute()
            
            if deleted_count == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Документ не найден"
                )
                
        return Response(status_code=status.HTTP_204_NO_CONTENT)
        
    except HTTPException as e:
        raise e
    except IntegrityError as ie:
        transaction.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка целостности данных: {str(ie)}"
        )
    except Exception as e:
        if 'transaction' in locals():
            transaction.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка сервера: {str(e)}"
        )