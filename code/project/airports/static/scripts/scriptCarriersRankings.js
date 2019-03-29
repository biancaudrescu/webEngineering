var showData = new XMLHttpRequest();
var data;
console.log("hiii");
showData.open('GET', 'http://localhost:8000/rankings/?ndc=1&ndla=1&mdc=1&mdla=1&format=json', false);

showData.onload = function () {
    data = JSON.parse(showData.response);
    console.log(showData.responseText);
    //console.log(data);

}
showData.send();

function myFunction() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}


function update() {

     var mdc = document.getElementById("mdc");
    var strmdc = mdc.options[mdc.selectedIndex].value;
     var mdla = document.getElementById("mdla");
    var strmdla = mdla.options[mdla.selectedIndex].value;
     var ndc = document.getElementById("ndc");
    var strndc = ndc.options[ndc.selectedIndex].value;
     var ndla = document.getElementById("ndla");
    var strndla = ndla.options[ndla.selectedIndex].value;

    var showData1 = new XMLHttpRequest();
        var data1;
        console.log("hii2");
        var ss;
        ss='http://localhost:8000/rankings/?format=json';

        ss=ss+'&mdc='+strmdc+'&mdla='+strmdla+'&ndc='+strndc+'&ndla='+strndla;

            showData1.open('GET', ss, false);

        showData1.send();
        console.log(showData1.responseText);
        data1 = JSON.parse(showData1.response);


         var table_body = '<table width="100%"><thead><tr>  <th>carrier</th>\n' +
             '                      <th>min_del_carrier</th>\n' +
             '                    <th>min_del_late_air</th>\n' +
             '                    <th>num_del_carrier</th>\n' +
             '                    <th>num_del_late_air</th></tr></thead><tbody>';
        for (k in data1) {

            table_body += '<tr>';
            table_body += '<td>';
            table_body += data1[k]["carrier"] + '</br>';
            table_body += '</td>';

            table_body += '<td>';
            table_body += data1[k]["min_del_carrier"];
            table_body += '</td>';

            table_body += '<td>';
            table_body += data1[k]["min_del_late_air"];
            table_body += '</td>';

            table_body += '<td>';
            table_body += data1[k]["num_del_carrier"];
            table_body += '</td>';
            table_body += '<td>';

            table_body += data1[k]["num_del_late_air"];
            table_body += '</td>';
            table_body += '<td>';


        }
        table_body += '</tbody></table>';
        $('#myStatTable').html(table_body);


}

$(document).ready(function () {

    $("#menu-toggle").click(function (e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });


});
$(document).ready(function () {



        var k = 0;
        var table_body = '<table width="100%"><thead><tr> <th>carrier</th>\n' +
            '                      <th>min_del_carrier</th>\n' +
            '                    <th>min_del_late_air</th>\n' +
            '                    <th>num_del_carrier</th>\n' +
            '                    <th>num_del_late_air</th></tr></thead><tbody>';
        for (k in data) {

            table_body += '<tr>';
             table_body += '<td>';
            table_body += data[k]["carrier"] + '</br>';
            table_body += '</td>';

            table_body += '<td>';
            table_body += data[k]["min_del_carrier"];
            table_body += '</td>';

            table_body += '<td>';
            table_body += data[k]["min_del_late_air"];
            table_body += '</td>';

            table_body += '<td>';
            table_body += data[k]["num_del_carrier"];
            table_body += '</td>';
            table_body += '<td>';

            table_body += data[k]["num_del_late_air"];
            table_body += '</td>';
            table_body += '<td>';


        }
        table_body += '</tbody></table>';
        $('#myStatTable').html(table_body);



    //display data..........


// for search function.................................. only............................
    $("#search").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("table tr").filter(function (index) {
            if (index > 0) {
                $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
            }
        });
    });

});

