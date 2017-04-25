import { Router } from 'express'
import example from 'src/routes/example'
import users from 'src/routes/users'
import eiei from 'src/routes/eiei'

const router = Router()

router.use('/', example)
router.use('/test', eiei)
router.use('/users', users)

export default router
