function sum() {
  var input1 = document.getElementById('input1').value || 0;
  var input2 = document.getElementById('input2').value || 0;
  document.getElementById('result').value = input1 + input2;
}