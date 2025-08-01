addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url)
  const slug = url.pathname.replace(/^\/+/, '') // remove barras iniciais

  // Exemplo: seu redirects.json está hospedado publicamente ou embutido
  // Aqui vamos carregar o redirects.json para pegar o link correspondente
  // Ideal: cachear para evitar buscar toda hora
  const redirectsUrl = 'https://yourdomain.com/path/to/redirects.json'
  let redirects

  try {
    const response = await fetch(redirectsUrl)
    redirects = await response.json()
  } catch (e) {
    return new Response('Error loading redirects', { status: 500 })
  }

  const linkInfo = redirects.links[slug]

  if (!linkInfo) {
    return new Response('Redirect not found', { status: 404 })
  }

  // Log click details (exemplo básico)
  const referrer = request.headers.get('referer') || 'direct'
  const userAgent = request.headers.get('user-agent') || 'unknown'
  const ip = request.headers.get('cf-connecting-ip') || 'unknown'
  const timestamp = new Date().toISOString()

  // Exemplo: envie esses dados para um endpoint (webhook, API, etc)
  // await fetch('https://your-logging-endpoint.com/log', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify({ slug, referrer, userAgent, ip, timestamp })
  // })

  // Para agora, só log no console (útil para debugging no dashboard Workers)
  console.log(`Click logged: ${slug} from ${referrer} ip:${ip} ua:${userAgent}`)

  // Redirecionar para o link afiliado
  return Response.redirect(linkInfo.affiliateLink, 302)
}
