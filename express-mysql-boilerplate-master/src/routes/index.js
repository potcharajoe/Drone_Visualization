import { Router } from 'express'
import drone_req from 'src/routes/drone_req'
import users from 'src/routes/users'


const router = Router()

router.use('/', drone_req)
router.use('/users', users)

export default router
