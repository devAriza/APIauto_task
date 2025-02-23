d = document;

const $btnAddTask = d.getElementById("btnAddTask")

const $modalCreateTask = d.getElementById("modalCreateTask")
const modalCreate = new bootstrap.Modal($modalCreateTask);

const $modalUpdateTask = d.getElementById("modalUpdateTask")
const modalUpdate = new bootstrap.Modal($modalUpdateTask)

const $modalDeleteTask = d.getElementById("modalDeleteTask")
const modalDelete = new bootstrap.Modal($modalDeleteTask)


function openModalCreate(){
    modalCreate.show();
}

function openModalUpdate(){
    modalUpdate.show();
}

function openModalDelete(){
    modalDelete.show();
}