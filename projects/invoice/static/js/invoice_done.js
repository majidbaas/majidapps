const invoice = document.querySelector(".invoice-wrapper");

document.getElementById("image").onclick = function(){

    html2canvas(invoice).then(canvas=>{

        let a=document.createElement("a");

        a.download="invoice.png";

        a.href=canvas.toDataURL();

        a.click();

    });

};

document.getElementById("pdf").onclick=function(){

    html2pdf()

    .set({

        margin:0,

        filename:"invoice.pdf",

        html2canvas:{scale:2},

        jsPDF:{

            unit:"mm",

            format:"a4",

            orientation:"portrait"

        }

    })

    .from(invoice)

    .save();

};