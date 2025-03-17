import { redirect } from 'next/navigation'

export default function Home() {
  // TODO: Check if the user is authenticated.
  redirect('/login')
}
