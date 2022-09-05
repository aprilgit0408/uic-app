const csrftoken = getCookie('csrftoken');
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie != '') {
        const cookie = document.cookie.split(';');
        for (let index = 0; index < cookie.length; index++) {
            const element = cookie[index].trim();
            if (element.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(element.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function getItems(id, url) {
    let parametros = {
        'action': 'searchdata'
    }
    console.log('valor de id: ', id);
    $(id).DataTable({
        responsive: true,
        language: {
            "lengthMenu": "Elementos _MENU_ por página",
            "zeroRecords": "Sin elementos que mostrar",
            "info": "Página _PAGE_ de _PAGES_",
            "search": "Buscar: ",
            "paginate": {
                "first": "Primero",
                "last": "Último",
                "next": "Siguiente",
                "previous": "Anterior"
            },
            "infoEmpty": "Sin Elementos",
            "infoFiltered": "(filtered from _MAX_ total records)"
        },
        autoWidth: false, // respetar anchos de columna
        destroy: true, // reiniciar con otro proceso
        deferRender: true,
        ajax: {
            url: '',
            type: 'POST',
            data: parametros,
            dataSrc: '',
            headers: {
                'X-CSRFToken': csrftoken
            }
        },
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let btn =  `
                    <div class="row" >
                        <div class="col-sm-6" style=" margin-right: -12px; ">
                            <a type="submit" href="edit/${row[row.length - 1]}" class="btn btn-outline-warning">Editar</a> 
                        </div>
                        <div class="col-sm-6" >
                            <a type="submit" href="delete/${row[row.length - 1]}" class="btn btn-outline-danger">Eliminar</a>
                        </div>
                    </div>
                    `;
                    return btn;
                }
            }
        ],
    })
};