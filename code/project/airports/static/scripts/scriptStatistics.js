var showData = new XMLHttpRequest();
var data;
console.log("hiii");
showData.open('GET', 'http://localhost:8000/airports/ATL/statistics/?c_code=AA&format=json', false);

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
    var ss='http://localhost:8000/airports/'+strairport+'/statistics/?c_code='+strcarrier+'&format=json&month_year='+strmonth;
     console.log(ss);
    if (strmonth === "ALL")
        showData1.open('GET', 'http://localhost:8000/airports/'+strairport+'/statistics/?c_code='+strcarrier+'&format=json', false);
    else
        showData1.open('GET', 'http://localhost:8000/airports/'+strairport+'/statistics/?c_code='+strcarrier+'&format=json&month_year='+strmonth, false);

showData1.send();
    data1 = JSON.parse(showData1.response);

console.log(showData1.responseText);

    var table_body = '<table width="100%"><thead><tr>\n' +
        '                    <th>#Cancelled</th>\n' +
        '                    <th>#On time</th>\n' +
        '                    <th>#Total</th>\n' +
        '                    <th>#Delayed</th>\n' +
        '                    <th>#Diverted</th>\n' +
        '\n' +
        '\n' +
        '                    <th>#delay late aircraft</th>\n' +
        '                    <th>#delay weather</th>\n' +
        '                    <th>#delay security</th>\n' +
        '                    <th>#delay NAV</th>\n' +
        '                    <th>#delay carrier</th>\n' +
        '\n' +
        '                   <th>#minutes delay late aircraft</th>\n' +
        '                   <th>#minutes delay weather</th>\n' +
        '                   <th>#minutes delay carrier</th>\n' +
        '                   <th>#minutes delay security</th>\n' +
        '                   <th>#minutes delay total</th>\n' +
        '                    <th>#minutes delay NAV</th>\n' +
        '\n' +
        '\n' +
        '                  </tr></thead><tbody>';
    var k;
    for (k in data1) {

       table_body += '<tr id=k>';

        table_body += '<td>';
        table_body += data1[k]["statistics"]["flights"]["cancelled"];
        table_body += '</td>';

        table_body += '<td>';
         table_body += data1[k]["statistics"]["flights"]["on_time"];
        table_body += '</td>';


        table_body += '<td>';
        table_body += data1[k]["statistics"]["flights"]["total"];
        table_body += '</td>';


        table_body += '<td>';
         table_body += data1[k]["statistics"]["flights"]["delayed"];
        table_body += '</td>';


        table_body += '<td>';
         table_body += data1[k]["statistics"]["flights"]["diverted"];
        table_body += '</td>';


        table_body += '<td>';
         table_body += data1[k]["statistics"]["num_del"]["weather"];
        table_body += '</td>';


        table_body += '<td>';
       table_body += data1[k]["statistics"]["num_del"]["security"];
        table_body += '</td>';


        table_body += '<td>';
       table_body += data1[k]["statistics"]["num_del"]["late_aircraft"];
        table_body += '</td>';


        table_body += '<td>';
        table_body += data1[k]["statistics"]["num_del"]["nat_avi_sys"];
        table_body += '</td>';


        table_body += '<td>';
        table_body += data1[k]["statistics"]["num_del"]["carrier"];
        table_body += '</td>';


        table_body += '<td>';
         table_body += data1[k]["statistics"]["minutes_del"]["late_aircraft"];
        table_body += '</td>';


        table_body += '<td>';
       table_body += data1[k]["statistics"]["minutes_del"]["weather"];
        table_body += '</td>';


        table_body += '<td>';
       table_body += data1[k]["statistics"]["minutes_del"]["carrier"];
        table_body += '</td>';


        table_body += '<td>';
        table_body += data1[k]["statistics"]["minutes_del"]["security"];
        table_body += '</td>';


        table_body += '<td>';
        table_body += data1[k]["statistics"]["minutes_del"]["total"];
        table_body += '</td>';


        table_body += '<td>';
        table_body += data1[k]["statistics"]["minutes_del"]["nat_avi_sys"];
        table_body += '</td>';

        table_body += '<button id=k>B1</button>'
        table_body += '</tr>';

    }
    table_body += '</tbody></table>';
    $('#myStatTable').html(table_body);


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
    var table_body = '<table width="100%"><thead><tr>\n' +
        '                    <th>#Cancelled</th>\n' +
        '                    <th>#On time</th>\n' +
        '                    <th>#Total</th>\n' +
        '                    <th>#Delayed</th>\n' +
        '                    <th>#Diverted</th>\n' +
        '\n' +
        '\n' +
        '                    <th>#delay late aircraft</th>\n' +
        '                    <th>#delay weather</th>\n' +
        '                    <th>#delay security</th>\n' +
        '                    <th>#delay NAV</th>\n' +
        '                    <th>#delay carrier</th>\n' +
        '\n' +
        '                   <th>#minutes delay late aircraft</th>\n' +
        '                   <th>#minutes delay weather</th>\n' +
        '                   <th>#minutes delay carrier</th>\n' +
        '                   <th>#minutes delay security</th>\n' +
        '                   <th>#minutes delay total</th>\n' +
        '                    <th>#minutes delay NAV</th>\n' +
        '\n' +
        '\n' +
        '                  </tr></thead><tbody>';
    for (k in data) {

        table_body += '<tr>';

        table_body += '<td>';
        table_body += data[k]["statistics"]["flights"]["cancelled"];
        table_body += '</td>';

        table_body += '<td>';
         table_body += data[k]["statistics"]["flights"]["on_time"];
        table_body += '</td>';


        table_body += '<td>';
        table_body += data[k]["statistics"]["flights"]["total"];
        table_body += '</td>';


        table_body += '<td>';
         table_body += data[k]["statistics"]["flights"]["delayed"];
        table_body += '</td>';


        table_body += '<td>';
         table_body += data[k]["statistics"]["flights"]["diverted"];
        table_body += '</td>';


        table_body += '<td>';
         table_body += data[k]["statistics"]["num_del"]["weather"];
        table_body += '</td>';


        table_body += '<td>';
       table_body += data[k]["statistics"]["num_del"]["security"];
        table_body += '</td>';


        table_body += '<td>';
       table_body += data[k]["statistics"]["num_del"]["late_aircraft"];
        table_body += '</td>';


        table_body += '<td>';
        table_body += data[k]["statistics"]["num_del"]["nat_avi_sys"];
        table_body += '</td>';


        table_body += '<td>';
        table_body += data[k]["statistics"]["num_del"]["carrier"];
        table_body += '</td>';


        table_body += '<td>';
         table_body += data[k]["statistics"]["minutes_del"]["late_aircraft"];
        table_body += '</td>';


        table_body += '<td>';
       table_body += data[k]["statistics"]["minutes_del"]["weather"];
        table_body += '</td>';


        table_body += '<td>';
       table_body += data[k]["statistics"]["minutes_del"]["carrier"];
        table_body += '</td>';


        table_body += '<td>';
        table_body += data[k]["statistics"]["minutes_del"]["security"];
        table_body += '</td>';


        table_body += '<td>';
        table_body += data[k]["statistics"]["minutes_del"]["total"];
        table_body += '</td>';


        table_body += '<td>';
        table_body += data[k]["statistics"]["minutes_del"]["nat_avi_sys"];
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

    $
});




