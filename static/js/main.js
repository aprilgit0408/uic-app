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
    let table = $(id).DataTable({
        responsive: true,
        fixedHeader: {
            header: true,
            footer: true
        },
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
            "loadingRecords": "Cargando...",
            "processing": "Procesando...",
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
                    let btn = data;
                    if(data === 'descargarArchivo'){
                        btn = `
                            <div class="row" >
                                <div class="col-md-6" >
                                    <a type="submit" href="${row[row.length - 1]}" class="btn btn-outline-info" target="_blank" title="Ver/Descargar Archivo" >
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-download" viewBox="0 0 16 16">
                                    <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
                                    <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/>
                                    </svg>
                                    </a>
                                </div>
                            </div>
                            `;
                        return btn;
                    }
                    if(data === 'file'){
                        let url = row[row.length - 2];
                        tipo = '';
                        color = '';
                        if(url === 'pdf'){
                            tipo = `
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-filetype-pdf" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M14 4.5V14a2 2 0 0 1-2 2h-1v-1h1a1 1 0 0 0 1-1V4.5h-2A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v9H2V2a2 2 0 0 1 2-2h5.5L14 4.5ZM1.6 11.85H0v3.999h.791v-1.342h.803c.287 0 .531-.057.732-.173.203-.117.358-.275.463-.474a1.42 1.42 0 0 0 .161-.677c0-.25-.053-.476-.158-.677a1.176 1.176 0 0 0-.46-.477c-.2-.12-.443-.179-.732-.179Zm.545 1.333a.795.795 0 0 1-.085.38.574.574 0 0 1-.238.241.794.794 0 0 1-.375.082H.788V12.48h.66c.218 0 .389.06.512.181.123.122.185.296.185.522Zm1.217-1.333v3.999h1.46c.401 0 .734-.08.998-.237a1.45 1.45 0 0 0 .595-.689c.13-.3.196-.662.196-1.084 0-.42-.065-.778-.196-1.075a1.426 1.426 0 0 0-.589-.68c-.264-.156-.599-.234-1.005-.234H3.362Zm.791.645h.563c.248 0 .45.05.609.152a.89.89 0 0 1 .354.454c.079.201.118.452.118.753a2.3 2.3 0 0 1-.068.592 1.14 1.14 0 0 1-.196.422.8.8 0 0 1-.334.252 1.298 1.298 0 0 1-.483.082h-.563v-2.707Zm3.743 1.763v1.591h-.79V11.85h2.548v.653H7.896v1.117h1.606v.638H7.896Z"/>
                            </svg>
                            `;
                            color = 'danger';
                        }else if(url === 'xlsx' || url === 'xls'){
                            tipo = `
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-filetype-xlsx" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M14 4.5V11h-1V4.5h-2A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v9H2V2a2 2 0 0 1 2-2h5.5L14 4.5ZM7.86 14.841a1.13 1.13 0 0 0 .401.823c.13.108.29.192.479.252.19.061.411.091.665.091.338 0 .624-.053.858-.158.237-.105.416-.252.54-.44a1.17 1.17 0 0 0 .187-.656c0-.224-.045-.41-.135-.56a1.002 1.002 0 0 0-.375-.357 2.028 2.028 0 0 0-.565-.21l-.621-.144a.97.97 0 0 1-.405-.176.37.37 0 0 1-.143-.299c0-.156.061-.284.184-.384.125-.101.296-.152.513-.152.143 0 .266.023.37.068a.624.624 0 0 1 .245.181.56.56 0 0 1 .12.258h.75a1.093 1.093 0 0 0-.199-.566 1.21 1.21 0 0 0-.5-.41 1.813 1.813 0 0 0-.78-.152c-.293 0-.552.05-.777.15-.224.099-.4.24-.527.421-.127.182-.19.395-.19.639 0 .201.04.376.123.524.082.149.199.27.351.367.153.095.332.167.54.213l.618.144c.207.049.36.113.462.193a.387.387 0 0 1 .153.326.512.512 0 0 1-.085.29.558.558 0 0 1-.255.193c-.111.047-.25.07-.413.07-.117 0-.224-.013-.32-.04a.837.837 0 0 1-.249-.115.578.578 0 0 1-.255-.384h-.764Zm-3.726-2.909h.893l-1.274 2.007 1.254 1.992h-.908l-.85-1.415h-.035l-.853 1.415H1.5l1.24-2.016-1.228-1.983h.931l.832 1.438h.036l.823-1.438Zm1.923 3.325h1.697v.674H5.266v-3.999h.791v3.325Zm7.636-3.325h.893l-1.274 2.007 1.254 1.992h-.908l-.85-1.415h-.035l-.853 1.415h-.861l1.24-2.016-1.228-1.983h.931l.832 1.438h.036l.823-1.438Z"/>
                          </svg>
                            `;
                            color = 'success';
                        }else{
                            tipo = `
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-word" viewBox="0 0 16 16">
                            <path d="M5.485 6.879a.5.5 0 1 0-.97.242l1.5 6a.5.5 0 0 0 .967.01L8 9.402l1.018 3.73a.5.5 0 0 0 .967-.01l1.5-6a.5.5 0 0 0-.97-.242l-1.036 4.144-.997-3.655a.5.5 0 0 0-.964 0l-.997 3.655L5.485 6.88z"/>
                            <path d="M14 14V4.5L9.5 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2zM9.5 3A1.5 1.5 0 0 0 11 4.5h2V14a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h5.5v2z"/>
                            </svg>
                            `;
                            color = 'primary';
                        }
                        if(row[4] === false || row[4] === null){
                            tipoBotonAOpen = `<button type="button" onClick="enviarDirector('${row[1]}')" class="btn btn-outline-${ row[4] === false || row[4] === null ? 'info' : 'secondary'}" title="Enviar al  Director"  ${ row[4] === false || row[4] === null ?' id="idEnviar" ' : 'disabled="true"'} ">`;
                            tipoBotonAClose= `</button>`;
                        }else{
                            tipoBotonAOpen = `<button type="button" class="btn btn-outline-${ row[4] === false || row[4] === null ? 'info' : 'secondary'}" title="Enviar al  Director"  ${ row[4] === false || row[4] === null ?' id="idEnviar" ' : 'disabled="true"'} ">`;
                            tipoBotonAClose= `</button>`;
                        }
                        btn = `
                            <div class="row" >
                                <div class="col-md-4">
                                    <a type="submit" href="${row[row.length - 1]}" class="btn btn-outline-${color}" title="Descargar Formato" >
                                    ${tipo}
                                    </a> 
                                </div>
                                <div class="col-md-4">
                                    <a type="submit" href="generar/${row[1]}" class="btn btn-outline-warning" title="Generar Archivo" target="_blank" >
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-arrow-down" viewBox="0 0 16 16">
                                    <path d="M8.5 6.5a.5.5 0 0 0-1 0v3.793L6.354 9.146a.5.5 0 1 0-.708.708l2 2a.5.5 0 0 0 .708 0l2-2a.5.5 0 0 0-.708-.708L8.5 10.293V6.5z"/>
                                    <path d="M14 14V4.5L9.5 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2zM9.5 3A1.5 1.5 0 0 0 11 4.5h2V14a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h5.5v2z"/>
                                    </svg>
                                    </a> 
                                </div>
                                <div class="col-md-4">
                                    ${tipoBotonAOpen}
                                    ${row[4] === true ? '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check-square-fill" viewBox="0 0 16 16"><path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm10.03 4.97a.75.75 0 0 1 .011 1.05l-3.992 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.75.75 0 0 1 1.08-.022z"/></svg>': row[4] === false ? '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-cursor" viewBox="0 0 16 16"><path d="M14.082 2.182a.5.5 0 0 1 .103.557L8.528 15.467a.5.5 0 0 1-.917-.007L5.57 10.694.803 8.652a.5.5 0 0 1-.006-.916l12.728-5.657a.5.5 0 0 1 .556.103zM2.25 8.184l3.897 1.67a.5.5 0 0 1 .262.263l1.67 3.897L12.743 3.52 2.25 8.184z"/></svg>' : '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check" viewBox="0 0 16 16"><path d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.267.267 0 0 1 .02-.022z"/></svg>'}
                                    ${tipoBotonAClose}
                                </div>
                            `
                            return btn;
                    }
                    if(!!row[row.length - 1]){
                        btn = `
                            <div class="row" >
                                <div class="col-md-6">
                                    <a type="submit" href="edit/${row[row.length - 1]}" class="btn btn-outline-warning" title="Editar Registro" >
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                                    <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                                    <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z"/>
                                    </svg>
                                    </a> 
                                </div>
                                <div class="col-md-6" >
                                    <button type="button" onClick="eliminarRegistro('${row[row.length - 1]}');" class="btn btn-outline-danger" title="Eliminar Registro" >
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bucket" viewBox="0 0 16 16">
                                    <path d="M2.522 5H2a.5.5 0 0 0-.494.574l1.372 9.149A1.5 1.5 0 0 0 4.36 16h7.278a1.5 1.5 0 0 0 1.483-1.277l1.373-9.149A.5.5 0 0 0 14 5h-.522A5.5 5.5 0 0 0 2.522 5zm1.005 0a4.5 4.5 0 0 1 8.945 0H3.527zm9.892 1-1.286 8.574a.5.5 0 0 1-.494.426H4.36a.5.5 0 0 1-.494-.426L2.58 6h10.838z"/>
                                    </svg>
                                    </button>
                                </div>
                            </div>
                            `;
                    }else if(row[row.length - 1] === false){
                        btn = `
                                <img src="${data}" width="100" height="100" >
                            `;
                    }
                    return btn;
                }
            }
        ],
    }).columns.adjust();;
    $('#container').css( 'display', 'block' );
    table.columns.adjust().draw();
};


function eliminarRegistro(datos){
    alertas('Alerta!', 'red', 'btn-red', '¿Está seguro de eliminar este registro?', 'Eliminar Registro', 'delete', datos, 'fa fa-trash');
}
function enviarDirector(datos){
    alertas('Perfecto..', 'blue', 'btn-blue', '¿Está seguro de enviar el archivo?', 'Continuar', 'enviar', datos, 'fa fa-send-o')
}
function guardarAprobacion(data){
    let estado = $('#guardarSolicitud'+data)[0].checked ? true : '';
    if(estado){
        alertas('Alerta', 'orange', 'btn-warning', '¿Está seguro de Aprobar esta solicitud?', 'Aceptar', 'solicitud', data, 'fa fa-warning')
    }else{
        alertas('Alerta', 'orange', 'btn-warning', '¿Está seguro de Rechazar esta solicitud?', 'Aceptar', 'solicitud', data, 'fa fa-warning')
    }
}

function alertas(titulo, tipo, btnClass, mensaje, boton, funcion, data, icon) {
    $.confirm({
        title: titulo,
        type: tipo,
        typeAnimated: true,
        content: mensaje,
        icon: icon,
        autoClose: 'Cancelar|9000',
        buttons: {
            tryAgain: {
                text: boton,
                btnClass: btnClass,
                action: function () {
                    if (funcion === 'solicitud') {
                        let estado = $('#guardarSolicitud'+data)[0].checked ? true : '';
                        $.ajax({
                            url: '',
                            method: 'POST',
                            data: {id: data, estado : estado},
                            headers: {
                                'X-CSRFToken': csrftoken
                            }
                        }).done((req) => {
                            console.log('Datos Guardados: ', req);
                        });
                    }
                    if (funcion === 'enviar') {
                        $.ajax({
                            url: `enviar/${data}`,
                            method: 'GET',
                            headers: {
                                'X-CSRFToken': csrftoken
                            }
                        }).done((req) => {
                            $.alert('Datos Enviados...');
                        });
                    }
                    if (funcion === 'delete') {
                        $.ajax({
                            url: `delete/${data}`,
                            method: 'DELETE',
                            headers: {
                                'X-CSRFToken': csrftoken
                            }
                        }).done((req) => {
                            console.log('Datos Guardados: ', req);
                            location.reload();
                        });
                    }
                }
            },
            Cancelar: function () {
                if(funcion === 'reload'){location.reload();}
                if(funcion === 'solicitud'){$('#guardarSolicitud'+data)[0].checked = !$('#guardarSolicitud'+data)[0].checked;}
            }
        },
        cancelar: function () {
        },
    });
}