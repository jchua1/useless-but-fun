var x;

document.addEventListener('DOMContentLoaded', function (e) {
	var socket = io();
	var canvasElement = document.getElementById('canvas');
	var game = Game.create(socket, canvasElement);
	x = game;

	Input.applyEventHandlers(canvasElement);
	Input.addMouseTracker(canvasElement);

	console.log('loaded');

	socket.emit('new_player', {
		name: 'test'
	}, function (data) {
		game.start();
	});
});
