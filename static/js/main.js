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
    let responsiveTable = !!url ? url : false;
    console.log('valor de id: ', id);
    let table = $(id).DataTable({
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
            "infoEmpty": "Ninguna coincidencia encontrada ",
            "infoFiltered": "en los _MAX_ registro actuales"
        },
        autoWidth: responsiveTable, // respetar anchos de columna
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
                    console.log('row: ', row);
                    console.log('row length : ', row.length);
                    let btn = data;
                    if(!!row[row.length - 1]){
                        btn = `
                            <div class="row" >
                                <div class="col-sm-6" style=" margin-right: -12px; ">
                                    <a type="submit" href="edit/${row[row.length - 1]}" class="btn btn-outline-warning">Editar</a> 
                                </div>
                                <div class="col-sm-6" >
                                    <a type="submit" href="delete/${row[row.length - 1]}" class="btn btn-outline-danger">Eliminar</a>
                                </div>
                            </div>
                            `;
                    }else if(row.length > 7 && !!(row[7].includes('media/') || row[7].includes('static/'))){
                        btn = `
                                <img src="${row[7]}" width="100" height="100" >
                            `;
                    }
                    return btn;
                }
            }
        ],
    });
    $('#container').css( 'display', 'block' );
    table.columns.adjust().draw();
};