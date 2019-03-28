var showData = new XMLHttpRequest();
var data;
console.log("hiii");
showData.open('GET', 'http://localhost:8000/comments/?format=json', false);

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


    var e = document.getElementById("locale");
    var strUser = e.options[e.selectedIndex].value;
    console.log(strUser);
    var showData1 = new XMLHttpRequest();
        var data1;
        console.log("hii2");


        if(strUser==="ALL")
            showData1.open('GET', 'http://localhost:8000/comments/?format=json', false);
        else
            showData1.open('GET', 'http://localhost:8000/comments/?carrier='+strUser+'&format=json', false);
        showData1.send();
        console.log(showData1.responseText);
        data1 = JSON.parse(showData1.response);


         var table_body = '<table width="100%"><thead><tr><th>Code</th><th>Comment</th></tr></thead><tbody>';
        for (k in data1) {

            table_body += '<tr>';
            table_body += '<td>';
            table_body += data1[k]["carrier"] + '</br>';
            table_body += '</td>';

            table_body += '<td>';
            table_body += data1[k]["comment"];
            table_body += '</td>';


            table_body += '</tr>';

        }
        table_body += '</tbody></table>';
        $('#myTable').html(table_body);


}

$(document).ready(function () {

    $("#menu-toggle").click(function (e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });


});
$(document).ready(function () {



        var k = 0;
        var table_body = '<table width="100%"><thead><tr><th>Code</th><th>Comment</th></tr></thead><tbody>';
        for (k in data) {

            table_body += '<tr>';
            table_body += '<td>';
            table_body += data[k]["carrier"] + '</br>';
            table_body += '</td>';

            table_body += '<td>';
            table_body += data[k]["comment"];
            table_body += '</td>';


            table_body += '</tr>';

        }
        table_body += '</tbody></table>';
        $('#myTable').html(table_body);



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

