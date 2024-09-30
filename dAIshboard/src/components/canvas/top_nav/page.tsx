
import { useParams } from 'react-router-dom'
import { Button } from '@/components/ui/button';
import { useNavigate } from 'react-router-dom';



export function TopNav() {

    const { user_id } = useParams()
    const navigate = useNavigate();
    const goToProjects = () => {
        let url = `/projects/${user_id}`
        navigate(url);
    }

    return <Button onClick={goToProjects}>Projects</Button>
}