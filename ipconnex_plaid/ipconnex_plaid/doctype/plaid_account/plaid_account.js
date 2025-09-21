var script = document.createElement("script");
script.src = "https://cdn.jsdelivr.net/npm/sweetalert2@10";
document.head.appendChild(script);

frappe.ui.form.on("Plaid Account", {
  refresh: function (frm) {
    $("button[data-fieldname='Update']")
      .off("click")
      .on("click", function () {
        frappe.call({
          method: "ipconnex_plaid.ipconnex_plaid.app.updatePlaidAccount",
          args: {
            doc_name: frm.doc.name,
          },
          callback: function (res) {
            if (res.message.status == 1) {
              frm.reload_doc();
              Swal.fire({
                icon: "success",
                title: "Success",
                text: res.message.message,
              });
            } else {
              Swal.fire({
                icon: "warning",
                title: "Warning",
                text: res.message.message,
              });
            }
          },
        });
      });
  },
});
