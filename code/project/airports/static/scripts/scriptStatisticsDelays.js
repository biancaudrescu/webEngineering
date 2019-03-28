var showData = new XMLHttpRequest();
var data;
console.log("hiii");
showData.open('GET', 'http://localhost:8000/airports/ALL/statistics/delays/?c_code=AA&format=json', false);

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

    var reason = document.getElementById("reason");
    var streason = reason.options[reason.selectedIndex].value;
    var month = document.getElementById("month");
    var strmonth = month.options[month.selectedIndex].value;
     var airport = document.getElementById("airport");
    var strairport = airport.options[airport.selectedIndex].value;
     var carrier = document.getElementById("carrier");
    var strcarrier = carrier.options[carrier.selectedIndex].value;
    console.log(strairport);
    console.log(strcarrier);
    console.log(strmonth);

    var showData1 = new XMLHttpRequest();
    var data1;
    console.log(strmonth);
    var ss;

    ss='http://localhost:8000/airports/'+strairport+'/statistics/delays/?c_code='+strcarrier+'&format=json';

    if (strmonth !== "ALL")
        ss=ss+'&month_year='+strmonth;
    if(streason!=="ALL")
        ss=ss+'&reason='+streason;
 console.log(ss);
        showData1.open('GET', ss, false);

showData1.send();
    data1 = JSON.parse(showData1.response);

console.log(showData1.responseText);
    if(streason!=="ALL") {
        var table_body = '<table width="100%"><thead><tr><th>lateAircraft</th>\n' +
            '     <th>carrier</th>\n</tr></thead><tbody>';
        var k;
        for (k in data1) {

            table_body += '<tr>';

            table_body += '<td>';
            table_body += data1[k]["late_airport"];
            table_body += '</td>';

            table_body += '<td>';
            table_body += data1[k]["carrier"];
            table_body += '</td>';


            table_body += '</tr>';

        }
        table_body += '</tbody></table>';
        $('#myStatTable').html(table_body);
    }
    else{

         var table_body = '<table width="100%"><thead><tr>  \n' +
             '                    <th>#delay NAV</th>\n' +
             '                    <th>#delay late aircraft</th>\n' +
             '                    <th>#delay weather</th>\n' +
             '                       <th>#delay carrier</th>\n' +
             '                    <th>#delay security</th>   </tr></thead><tbody>';

    for (k in data1) {

        table_body += '<tr>';

        table_body += '<td>';
        table_body += data1[k]["delays"]["nat_avi_sys"];
        table_body += '</td>';

        table_body += '<td>';
         table_body += data1[k]["delays"]["late_aircraft"];
        table_body += '</td>';



        table_body += '<td>';
         table_body += data1[k]["delays"]["weather"];
        table_body += '</td>';


        table_body += '<td>';
         table_body += data1[k]["delays"]["carrier"];
        table_body += '</td>';


        table_body += '<td>';
         table_body += data1[k]["delays"]["security"];
        table_body += '</td>';





        table_body += '</tr>';

    }
    table_body += '</tbody></table>';
    $('#myStatTable').html(table_body);


    }



}

$(document).ready(function () {

    $("#menu-toggle").click(function (e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });


});
$(document).ready(function () {


    var k = 0;
 var table_body = '<table width="100%"><thead><tr>  \n' +
             '                    <th>#delay NAV</th>\n' +
             '                    <th>#delay late aircraft</th>\n' +
             '                    <th>#delay weather</th>\n' +
             '                       <th>#delay carrier</th>\n' +
             '                    <th>#delay security</th>   </tr></thead><tbody>';
    for (k in data) {

        table_body += '<tr>';

        table_body += '<td>';
        table_body += data[k]["delays"]["nat_avi_sys"];
        table_body += '</td>';

        table_body += '<td>';
         table_body += data[k]["delays"]["late_aircraft"];
        table_body += '</td>';



        table_body += '<td>';
         table_body += data[k]["delays"]["weather"];
        table_body += '</td>';


        table_body += '<td>';
         table_body += data[k]["delays"]["carrier"];
        table_body += '</td>';


        table_body += '<td>';
         table_body += data[k]["delays"]["security"];
        table_body += '</td>';





        table_body += '</tr>';

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


$(document).ready(function () {
    $("#menu-toggle").click(function (e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    })


});
