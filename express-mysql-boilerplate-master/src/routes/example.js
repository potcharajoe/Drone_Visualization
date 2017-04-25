import { Router } from 'express'
import fs from 'fs'
import path from 'path'

const router = Router()


router.route('/')
		.get((req, res) => {
			console.log('HELLO')
		})

router.route('/station')
		.get((req, res) => {
			let data = JSON.parse(fs.readFileSync(path.join(__dirname,'../../', 'station.json'), 'utf8'))
			res.json(data)
		})

router.route('/point1')
		.get((req, res) => {
			let data = JSON.parse(fs.readFileSync(path.join(__dirname,'../../', 'point1.json'), 'utf8'))
			res.json(data)
		})

router.route('/point2')
		.get((req, res) => {
			let data = JSON.parse(fs.readFileSync(path.join(__dirname,'../../', 'point2.json'), 'utf8'))
			res.json(data)
		})


router.route('/point3')
		.get((req, res) => {
			let data = JSON.parse(fs.readFileSync(path.join(__dirname,'../../', 'point3.json'), 'utf8'))
			res.json(data)
		})

router.route('/point1_mode1')
		.get((req, res) => {
			let data = JSON.parse(fs.readFileSync(path.join(__dirname,'../../', 'point1_mode1.json'), 'utf8'))
			res.json(data)
		})

router.route('/point2_mode1')
		.get((req, res) => {
			let data = JSON.parse(fs.readFileSync(path.join(__dirname,'../../', 'point2_mode1.json'), 'utf8'))
			res.json(data)
		})


router.route('/point3_mode1')
		.get((req, res) => {
			let data = JSON.parse(fs.readFileSync(path.join(__dirname,'../../', 'point3_mode1.json'), 'utf8'))
			res.json(data)
		})

router.route('/point1_move')
		.get((req, res) => {
			let data = JSON.parse(fs.readFileSync(path.join(__dirname,'../../', 'gps_location1.json'), 'utf8'))
			res.json(data)
		})

router.route('/point2_move')
		.get((req, res) => {
			let data = JSON.parse(fs.readFileSync(path.join(__dirname,'../../', 'gps_location2.json'), 'utf8'))
			res.json(data)
		})


router.route('/point3_move')
		.get((req, res) => {
			let data = JSON.parse(fs.readFileSync(path.join(__dirname,'../../', 'gps_location3.json'), 'utf8'))
			res.json(data)
		})

router.route('/destination')
		.get((req, res) => {
			let data = JSON.parse(fs.readFileSync(path.join(__dirname,'../../', 'destination.json'), 'utf8'))
			res.json(data)
		})

router.route('/trace_result')
		.get((req, res) => {
			let data = JSON.parse(fs.readFileSync(path.join(__dirname,'../../', 'trace_res.json'), 'utf8'))
			res.json(data)
		})
		
export default router
