
import { useParams } from 'react-router-dom'
import { Button } from '@/components/ui/button';
import { useNavigate } from 'react-router-dom';
import { MetaNav } from '../meta_nav/page';


export function TopNav() {

    const { user_id } = useParams()
    const navigate = useNavigate();
    const goToProjects = () => {

        let url = `/projects/${user_id}`
        navigate(url);
    }

    return <div className='flex flex-col-1'>
        <Button onClick={goToProjects}>Projects</Button>
        <MetaNav />
    </div>
}