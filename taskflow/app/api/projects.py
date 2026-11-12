from fastapi import APIRouter, HTTPException, Response, status, Depends
from app.schemas.projects import ProjectGet, ProjectCreate, ProjectUpdate
from app.dependencies.common import pagination_params, sorting_params, get_current_user

router = APIRouter(prefix='/projects', tags=['Tasks'])

projects = [
    {"id": 1, "name": "TaskFlow"}
]



@router.get("/", response_model=list[ProjectGet])
async def get_projects(
    pagination: dict = Depends(pagination_params),
    sorting: dict = Depends(sorting_params),
    current_user: dict = Depends(get_current_user)
) -> list[ProjectGet]:

    offset = pagination["offset"]
    limit = pagination["limit"]

    sort_by = sorting["sort_by"]
    order = sorting["order"]

    sorted_projects = sorted(
        projects,
        key=lambda project: project.get(sort_by),
        reverse=(order == "desc")
    )

    return sorted_projects[offset:offset + limit]



@router.post('/', response_model=ProjectGet)
async def create_project(paylaod: ProjectCreate):
    new_id = max((project['id'] for project in projects), default=0) + 1
    new_project = {'id': new_id, 'name': paylaod.name}
    projects.append(new_project)
    return new_project



@router.get('/{project_id}', response_model=ProjectGet)
def get_project_by_id(project_id: int, name: str):
    for project in projects:
        if project['id'] == project_id and (name in project['name']):
            return project
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Проект не найден'
    )


@router.patch('/{project_id}', response_model=ProjectGet)
def update_project(project_id: int, payload: ProjectUpdate):
    for project in projects:
        if project['id'] == project_id:
            if payload.name is not None:
                project['name'] = payload.name
            return project
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Проект не найден'
    )


@router.delete('/{project_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int):
    for project in projects:
        if project['id'] == project_id:
            projects.remove(project)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Проект не найден'
    )
