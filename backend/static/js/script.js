let modalOpeners = document.getElementsByClassName("modal-open");
let modalClosers = document.getElementsByClassName("close");
let blockTriggers = document.getElementsByClassName("category-block__trigger");
let incomeEdits = document.getElementsByClassName("category__edit");
let transactionFormTogglers = document.getElementsByClassName("transaction-form-toggle");
let transactionFormClosers = document.getElementsByClassName("close-transaction-form");
let transactionsFeed = document.querySelector('.feed');
let chartCanvas = document.getElementById('chart');
let sourceSelects = document.querySelectorAll("select[name='source']");

let limitBottom = document.documentElement.offsetHeight - window.innerHeight;
let transactionsLoadind = false;
let nextPage = 2;
window.addEventListener("scroll",function(){
  if(nextPage <= pageCount && document.documentElement.scrollTop >= limitBottom && !transactionsLoadind) {
    loadMoreTransaction();
  }
});

if(chartCanvas) {
    loadChart();
}

function loadMoreTransaction() {
    transactionsLoadind = true;
    let xhr = new XMLHttpRequest();
    xhr.open('GET', '/?page=' + nextPage, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-url');
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.onreadystatechange = function () {
        if (this.readyState != 4) return;

        if (this.status != 200) {
            alert('ошибка: ' + (this.status ? this.statusText : 'запрос не удался'));
            return;
        }
        transactionsFeed.innerHTML += this.responseText;

        limitBottom = document.documentElement.offsetHeight - window.innerHeight;
        nextPage++;
        transactionsLoadind = false;
    }
    xhr.send();
}

function loadChart() {
    let data = chartCanvas.dataset;
    let xhr = new XMLHttpRequest();
    xhr.open('GET', "/chart-data/" + data.accountId, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-url');
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.onreadystatechange = function () {
        if (this.readyState != 4) return;

        if (this.status != 200) {
            alert('ошибка: ' + (this.status ? this.statusText : 'запрос не удался'));
            return;
        }
        var json = JSON.parse(this.responseText);

        var labels = [];
        var incomeData = [];
        var expenseData = [];

        for(var i of json.data) {
            labels.push(i.d);
            incomeData.push(i.income);
            expenseData.push(i.expense);
        }

        var data = {
            labels: labels,
            datasets: [{
                label: 'Income',
                backgroundColor: 'rgb(0, 255, 0)',
                borderColor: 'rgb(0, 255, 0)',
                data: incomeData
            },
            {
                label: 'Expense',
                backgroundColor: 'rgb(255, 0, 0)',
                borderColor: 'rgb(255, 0, 0)',
                data: expenseData
            }]
        };

        var config = {
            type: 'line',
            data,
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        };

        var myChart = new Chart(document.getElementById('chart'), config);
    }
    xhr.send();
}

function change_destination_options(element) {
    let destination = element.closest("form").querySelector("select[name='destination']");

    let xhr = new XMLHttpRequest();
    xhr.open('GET', '/get-accounts-by-source?source=' + element.value);

    xhr.onload = function () {
        if (this.status != 200) {
            alert(this.status + ': ' + this.statusText);
        } else {
            let json = JSON.parse(this.responseText);
            updateOptions(destination, json.accounts);
        }
    }

    xhr.send();
}

function updateOptions(element, accounts) {
    element.innerHTML = "<option value='' disabled selected>----------</option>";
    for (let account of accounts) {
        let option = document.createElement("option");
        option.value = account.id;
        option.text = account.name;
        element.appendChild(option);
    }
}

for (let i = 0; i < modalOpeners.length; i++) {
    modalOpeners[i].onclick = function () {
        let modal = document.getElementById(this.dataset.target);
        modal.classList.remove("hide");
    }
}

for (let i = 0; i < modalClosers.length; i++) {
    modalClosers[i].onclick = function () {
        this.closest(".modal").classList.add("hide");
    }
}

for (let i = 0; i < blockTriggers.length; i++) {
    blockTriggers[i].onclick = function () {
        this.classList.toggle("category-block__trigger-opened");
        let categories = this.parentNode.querySelectorAll(".category");

        let showCount = categories[0].classList.contains("category-expense") ? 12 : 4;

        for (let i = showCount; i < categories.length; i++) {
            categories[i].classList.toggle("category__hidden");
        }
    }
}

for (let i = 0; i < incomeEdits.length; i++) {
    incomeEdits[i].onclick = function () {
        let data = this.dataset;

        let modal = document.getElementById(`modal-edit-${data.type}`);

        let xhr = new XMLHttpRequest();
        xhr.open('GET', '/edit-account/' + data.id);

        xhr.onload = function () {
            if (xhr.status != 200) {
                alert(xhr.status + ': ' + xhr.statusText);
            } else {
                let json = JSON.parse(xhr.responseText);
                modal.querySelector("form").setAttribute("action", `/edit-account/${data.id}/`);
                for (let field in json) {
                    let input = modal.querySelector(`input[name='${field}']`);
                    if (input != null) {
                        input.value = json[field];
                    }
                }
                modal.classList.remove("hide");
            }
        }

        xhr.send();
    }
}

for (let i = 0; i < transactionFormTogglers.length; i++) {
    transactionFormTogglers[i].onclick = function () {
        let transaction = this.closest(".transaction");
        transaction.querySelector(".transaction__view").classList.toggle("hide");
        transaction.querySelector(".transaction__edit").classList.toggle("hide");
    }
}

for (let i = 0; i < transactionFormClosers.length; i++) {
    transactionFormClosers[i].onclick = function () {
        let transaction = this.closest(".transaction");
        transaction.querySelector(".transaction__view").classList.toggle("hide");
        transaction.querySelector(".transaction__edit").classList.toggle("hide");
    }
}