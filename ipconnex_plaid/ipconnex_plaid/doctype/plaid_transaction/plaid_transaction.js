var script = document.createElement("script");
script.src = "https://cdn.jsdelivr.net/npm/sweetalert2@10";
document.head.appendChild(script);

function copyTextToClipboard(text) {
  var textarea = document.createElement("textarea");
  textarea.value = text;
  document.body.appendChild(textarea);
  textarea.select();
  document.execCommand("copy");
  document.body.removeChild(textarea);
}

frappe.ui.form.on("Plaid Transaction", {

});
