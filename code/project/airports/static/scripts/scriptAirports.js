







 var showData = new XMLHttpRequest();
        var data;
        console.log("hiii");
        showData.open('GET', 'http://localhost:8000/airports/?format=json',false);

        showData.onload = function(){
             data = JSON.parse(showData.response);
            console.log(showData.responseText);
            console.log(data);

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

$(document).ready(function(){

  $("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
  });


});
   $(document).ready(function(){

                var number_of_rows = data.length;
                var k = 0;
                var table_body = '<table width="100%"><thead><tr><th>Name</th><th>Code</th></tr></thead><tbody>';
                for(k in data){

                        table_body+='<tr>';
                        table_body +='<td>';
                        table_body +=data[k]["name"] ;
                        table_body +='</td>';

                        table_body +='<td>';
                        table_body +=data[k]["code"];
                        table_body +='</td>';


                        table_body+='</tr>';

                }
                table_body+='</tbody></table>';
                $('#myTable').html(table_body);
                //display data..........


// for search function.................................. only............................
            $("#search").on("keyup", function() {
                var value = $(this).val().toLowerCase();
                $("table tr").filter(function(index) {
                    if(index>0){
                        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
                    }
                });
            });




        });


