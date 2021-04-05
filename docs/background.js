var counter = 0;
function increment() {
	counter++;
	document.getElementById("counter").textContent = `Congratulations! You've built ${counter} robots!`;
}

function pullData() {
	const api_url = "http://127.0.0.1:5000/show";
	var response = await fetch(api_url, {method: 'POST'});
	scores = JSON.parse(response);
	return scores;
	/*
	return {
		"Forrest": Math.trunc(100 * Math.random()),
		"Eric": Math.trunc(100 * Math.random()),
		"Adam": Math.trunc(100 * Math.random()),
		"David": Math.trunc(100 * Math.random()),
		"Kyler": Math.trunc(100 * Math.random()),
		"Uday": Math.trunc(100 * Math.random()),
	};
	*/
}

function updateData() {
	let scores = pullData();
	scores = dictonarySort(scores);
	let table = document.getElementById("scores").getElementsByTagName('tbody')[0];


	clearData(table);

	for (var i = 0; i < scores.length; i++) {
		let name = scores[i][0];
		let score = scores[i][1];
		let newRow = table.insertRow(table.rows.length);

		// set #
		let placeCell = newRow.insertCell(0);
		placeCell.appendChild(document.createTextNode(i+1));
		// set name
		let nameCell = newRow.insertCell(1);
		nameCell.appendChild(document.createTextNode(name));
		// set score
		let scoreCell = newRow.insertCell(2);
		scoreCell.appendChild(document.createTextNode(score));
	}
	// table.add
}

function dictonarySort(dict) {
	// Create items array
	var items = Object.keys(dict).map(function (key) {
		return [key, dict[key]];
	});

	// Sort the array based on the second element
	items.sort(function (first, second) {
		return second[1] - first[1];
	});

	return items;
}

function clearData(table) {
	for (i = table.rows.length - 1; i >= 0; i--) {
		table.deleteRow(i);
	}
}

setInterval(updateData, 1000);