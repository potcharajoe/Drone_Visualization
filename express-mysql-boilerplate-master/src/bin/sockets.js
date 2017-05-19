import SocketIO from 'socket.io'
import fs from 'fs'
import path from 'path'


let sockets = {}

sockets.init = (server) => {
	const io = new SocketIO(server)
	io.on('connect', (socket) => {
		console.log('connect')

		
		socket.on('drone', (response) => {
			console.log(`${response}`)
		})

		setInterval( ()=> {
			let data = JSON.parse(fs.readFileSync(path.join(__dirname,'../../../', 'station.json'), 'utf8'))
			socket.emit('station', data)
			// let data1 = JSON.parse(fs.readFileSync(path.join(__dirname,'../../', 'gps_location1.json'), 'utf8'))
			// socket.emit('drone1', data1)
			// let data2 = JSON.parse(fs.readFileSync(path.join(__dirname,'../../', 'gps_location2.json'), 'utf8'))
			// socket.emit('drone2', data2)
			// let data3 = JSON.parse(fs.readFileSync(path.join(__dirname,'../../', 'gps_location3.json'), 'utf8'))
			// socket.emit('drone3', data3)
			let data4 = JSON.parse(fs.readFileSync(path.join(__dirname,'../../../', 'destination.json'), 'utf8'))
			socket.emit('destination', data4)
			let data5 = JSON.parse(fs.readFileSync(path.join(__dirname,'../../../', 'trace_res.json'), 'utf8'))
			socket.emit('trace', data5)

		},500)
	})
}

export default sockets
