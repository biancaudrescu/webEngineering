var showData = new XMLHttpRequest();
var data;
console.log("hiii");
showData.open('GET', 'http://localhost:8000/airports/ATL/statistics/description/?to=BOS&format=json', false);

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

    var airport1 = document.getElementById("airport1");
    var strairport1 = airport1.options[airport1.selectedIndex].value;
    var airport2 = document.getElementById("airport2");
    var strairport2 = airport2.options[airport2.selectedIndex].value;
    var carrier = document.getElementById("carrier");
    var strcarrier = carrier.options[carrier.selectedIndex].value;
    console.log(strairport1);


    var showData1 = new XMLHttpRequest();
    var data1;

    if (strcarrier === "ALL")
        showData1.open('GET', 'http://localhost:8000/airports/'+strairport1+'/statistics/description/?to='+strairport2+'&format=json', false);
    else
        showData1.open('GET', 'http://localhost:8000/airports/'+strairport1+'/statistics/description/?to='+strairport2+'&carrier='+strcarrier+'&format=json', false);

showData1.send();
    data1 = JSON.parse(showData1.response);

console.log(showData1.responseText);

    var table_body = '<table width="100%"><thead><tr> <th>carrier avg</th>\n' +
        '                    <th>carrier median</th>\n' +
        '                    <th>carrier std</th>\n' +
        '\n' +
        '                    <th>late aircraft avg</th>\n' +
        '                    <th>late aircraft median</th>\n' +
        '                    <th>late aircraft std</th></tr></thead><tbody>';
    
       table_body += '<tr id=k>';
 table_body += '<tr>';

        table_body += '<td>';
        table_body += data1["carrier"]["avg"];
        table_body += '</td>';

        table_body += '<td>';
         table_body += data1["carrier"]["median"];
        table_body += '</td>';


        table_body += '<td>';
        table_body += data1["carrier"]["std"];
        table_body += '</td>';


        table_body += '<td>';
         table_body += data1["late_aircraft"]["avg"];
        table_body += '</td>';


        table_body += '<td>';
         table_body += data1["late_aircraft"]["median"];
        table_body += '</td>';


        table_body += '<td>';
         table_body += data1["late_aircraft"]["std"];
        table_body += '</td>';


        table_body += '</tr>';
        table_body += '</tr>';

    
    table_body += '</tbody></table>';
    $('#myStatTable').html(table_body);
    $("#myStatTable").SetEditable({

    });

    $("button").click(function() {
    console.log(this.showData); // or alert($(this).attr('id'));
    });


}

$(document).ready(function () {

    $("#menu-toggle").click(function (e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });


});
$(document).ready(function () {


    var k = 0;
    var table_body = '<table width="100%"><thead><tr> <th>carrier avg</th>\n' +
        '                    <th>carrier median</th>\n' +
        '                    <th>carrier std</th>\n' +
        '\n' +
        '                    <th>late aircraft avg</th>\n' +
        '                    <th>late aircraft median</th>\n' +
        '                    <th>late aircraft std</th></tr></thead><tbody>';
        table_body += '<tr id=k>';
        table_body += '<tr>';
       
               table_body += '<td>';
               table_body += data["carrier"]["avg"];
               table_body += '</td>';
       
               table_body += '<td>';
                table_body += data["carrier"]["median"];
               table_body += '</td>';
       
       
               table_body += '<td>';
               table_body += data["carrier"]["std"];
               table_body += '</td>';
       
       
               table_body += '<td>';
                table_body += data["late_aircraft"]["avg"];
               table_body += '</td>';
       
       
               table_body += '<td>';
                table_body += data["late_aircraft"]["median"];
               table_body += '</td>';
       
       
               table_body += '<td>';
                table_body += data["late_aircraft"]["std"];
               table_body += '</td>';
       
       
               table_body += '</tr>';
               table_body += '</tr>';
       
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


$(document).ready(function () {
    $("#menu-toggle").click(function (e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    })

    $("#myStatTable").SetEditable({
        onEdit:function() {

        }
    });
});

