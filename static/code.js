$('#departamento').change(function() {
    //xx = "" + $(this).val();
    //console.log(xx);
    var y = document.getElementById("municipio");
    //e.preventDefault(); // avoid to execute the actual submit of the form.
    console.log('jijijiji');
    var form = document.getElementById("idFormpatentes");
    //var y = document.getElementById("reporte1");
    //y.innerHTML = '<p>...Ejecutando...';
    var data = new FormData(form);
    /*
    var x = document.getElementById("divspinner");
   
    if (x.style.display === "none") {
        x.style.display = "block";
    }
    */
    $.ajax({
        type: "POST",
        enctype: 'application/x-www-form-urlencoded',
        url: '/getmunis',
        data: data, // serializes the form's elements.
        processData: false,
        contentType: false,
        cache: false,
        success: function(data) {
            console.log(data); // show response from the php script.
            y.innerHTML = data;
        }
    });




});