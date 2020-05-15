function myFunction() {
    var x = document.getElementById("divspinner");
    var y = document.getElementById("divtable");
    var frec = document.getElementById("inputLarge");

    var dataa = 0;

    if (document.getElementById("customRadio1").checked) {
        dataa = { frecuencia: frec.value, tipo: 1 };
    } else {

        dataa = { frecuencia: frec.value, tipo: 0 };
    }
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {

    }
    $.ajax({
            method: "POST",
            url: "http://localhost:8080/generar",
            data: dataa
        })
        .done(function(msg) {
            x.style.display = "none";
            y.innerHTML += msg;
            console.log(msg);
            y.style.display = "block";

        });
}

function uploadd() {
    var x = document.getElementById("inputGroupFile02");
    var formdata = new FormData();
    var file = x.files[0];
    formdata.append("file", file);
    $.ajax({
            method: "POST",
            url: "http://localhost:8080/filtrar",
            data: file,
            processData: false,
            contentType: false
        })
        .done(function(msg) {
            console.log(msg);
        });

}

const data_mun = new Map()

data_mun.set(1, [
  [1, "Ciudad de Guatemala"],
  [51, "Santa Catarina Pinula"],
  [52, "San José Pinula"],
  [53, "San José del Golfo"],
  [54, "Palencia"],
  [55, "Chinautla"],
  [56, "San Pedro Ayampuc"],
  [57, "Mixco"],
  [58, "San Pedro Sacatepéquez"],
  [59, "San Juan Sacatepéquez"],
  [60, "San Raymundo"],
  [62, "Fraijanes"],
  [63, "Amatitlán"],
  [64, "Villa Nueva"],
  [65, "Villa Canales"],
  [66, "San Miguel Petapa"]
  ]);

data_mun.set(2, [
  [1, "Guastatoya"],
  [7, "Sanarate"],
  [8, "San Antonio La Paz"]
]);

data_mun.set(3, [
  [1, "Antigua Guatemala"],
  [2, "Jocotan"],
  [3, "Pastores"],
  [4, "Sumpango"],
  [5, "Santo Domingo Xenacoj"],
  [6, "Santiago Sacatepequéz"],
  [7, "San Bartolome Milpas Altas"],
  [8, "San Lucas Sacatepéquez"],
  [9, "Santa Lucia Milpas Altas"],
  [10, "Magdalena Milpas Altas"],
  [11, "Santa María de Jesús"],
  [12, "Ciudad Vieja"],
  [13, "San Martin Jilotepeque"],
  [14, "San Juan Alotenango"],
  [15, "San Antonio Aguas Calientes"]
]);

data_mun.set(4, [
  [1, "Chimaltenango"],
  [3, "San Martin Jilotepeque"],
  [4, "Comalapa"],
  [5, "Santa Apolonia"],
  [7, "Patzun"],
  [6, "Tecpan Guatemala"],
  [9, "Patzicia"],
  [10, "Santa Cruz Balanya"],
  [11, "Acatenango"],
  [12, "San Pedro Yepocapa"],
  [13, "San Andres Itzapa"],
  [14, "Parramos"],
  [15, "Zaragoza"],
  [16, "El Tejar"]
]);

data_mun.set(5, [
  [1,"Escuintla"],
  [2, "Santa Lucía Cotzulmalguapa"],
  [6, "Tiquisate"],
  [9, "Puerto de San José"],
  [11, "Palin"],
  [12, "San Vicente Pacaya"],
  [13, "Nueva Concepción"]
]);

data_mun.set(6, [
  [1, "Cuilapa"],
  [2, "Barberena"],
  [3, "Santa Rosa de Lima"],
  [6, "Oratorio"],
  [8, "Chiquimulilla"],
  [9, "Taxisco"],
  [10, "Santa María Ixhuatan"],
  [12, "Santa Cruz Naranjo"],
  [13, "Pueblo Nuevo Viñas"]
])

data_mun.set(7, [
  [1, "Solola"],
  [10, "Panajachel"],
  [13, "San Lucas Toliman"],
  [19, "Santiago Atitlan"]
]);

data_mun.set(8, [
  [1, "Totonicapan"],
  [3, "San Francisco El Alto"]
]);

data_mun.set(9, [
  [1, "Quetzaltenango"],
  [2, "Salcaja"],
  [4, "San Carlos Sija"],
  [14, "Cantel"],
  [20, "Coatepeque"],
  [21, "Genova"]
]);

data_mun.set(10, [
  [1, "Mazatenango"],
  [7, "San Lorenzo"],
  [10, "San Antonio Suchitepéquez"],
  [14, "Patulul"]
]);

data_mun.set(11, [
  [1, "Retalhuleu"],
  [2, "San Sebastian"],
  [4, "San Martín Zapotitlán"],
  [5, "San Felipe Retalhuleu"]
]);

data_mun.set(12, [
  [1, "San Marcos"],
  [2, "San Pedro Sacatepéquez"],
  [15, "Malacatan"],
  [16, "Catarina"],
  [18, "Ocos"],
  [23, "Ixchiguan"]
]);

data_mun.set(13, [
  [1, "Huehuetenango"],
  [7, "Jacaltenango"]
]);

data_mun.set(14, [
  [1, "Santa Cruz del Quiche"],
  [4, "Zacualpa"],
  [6, "Santo Tomas Chichicastenango"],
  [11, "San Juan Cotzal"],
  [12, "Joyabaj"],
  [13, "Santa María Nebaj"],
  [19, "Ixcan"]
]);

data_mun.set(15, [
  [1, "Salama"],
  [3, "Rabinal"],
  [4, "Cubulco"],
]);

data_mun.set(16, [
  [1, "Coban"],
  [2, "Santa Cruz Verapaz"],
  [9, "San Pedro Carcha"],
  [15, "Fray Bartolome de las Casas"]
]);

data_mun.set(17, [
  [1, "Flores"],
  [3, "San Benito"],
  [9, "San Francisco"],
  [12, "Poptun"]
]);

data_mun.set(18, [
  [1, "Puerto Barrios"]
]);

data_mun.set(19, [
  [1, "Zacapa"],
  [2, "Estanzuela"],
  [3, "Río Hondo"],
  [4, "Gualan"],
  [5, "Teculutan"],
  [7, "Cabañas"]
]);

data_mun.set(20, [
  [1, "Chiquimula"],
  [4, "Jocotan"],
  [5, "Camotan"],
  [7, "Esquipulas"],
  [11, "Ipala"]
]);

data_mun.set(21, [
  [1, "Jalapa"],
  [3, "San Luis Jilotepeque"]
]);

data_mun.set(22,[
  [1, "Jutiapa"],
  [4, "Agua Blanca"],
  [5, "Asunción Mita"],
  [7, "Atescatempa"],
  [8, "Jerez"],
  [11, "Comalapa"],
  [12, "Jalpatagua"],
  [14, "Moyuta"]
]);

const s_dep = document.querySelector('#depto');

s_dep.addEventListener('change', (event)=>{
  let valor = event.target.value;
  poblar(valor);
});


function poblar(valor) {
  let mun = data_mun.get(parseInt(valor));
  let select = document.querySelector('#mun');

  while (select.length > 0) {
    select.remove(select.length - 1);
  }

  mun.forEach(function(elem) {
    let opt = document.createElement("option");
    let txt = document.createTextNode(elem[1]);
    opt.setAttribute("value", elem[0]);
    opt.appendChild(txt)
    select.add(opt);
  });

}
