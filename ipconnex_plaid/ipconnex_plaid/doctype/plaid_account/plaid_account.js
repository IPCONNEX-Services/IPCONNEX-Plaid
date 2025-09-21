var script = document.createElement("script");
script.src = "https://cdn.jsdelivr.net/npm/sweetalert2@10";
document.head.appendChild(script);

frappe.ui.form.on("Plaid Account", {
  refresh: function (frm) {
    frm.add_custom_button(__("Update"), function (event) {
      $('button[data-label="Pay%20Invoice"]').prop("disabled", true);
      frappe.call({
        method: "ipconnex_plaid.ipconnex_plaid.app.updatePlaidAccount",
        args: {
          doc_name: frm.doc.name,
        },
        callback: function (res) {
          $('button[data-label="Pay%20Invoice"]').prop("disabled", false);
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
