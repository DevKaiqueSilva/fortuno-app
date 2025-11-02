describe('Authentication', () => {

  it('Should login with valid infos', () => {
    cy.visit('/login')
    cy.wait(500)
    cy.fixture('user').then((user) => {
      cy.login(user.testUser.email, user.testUser.password)
      cy.contains('Contas').should('be.visible')
    })
  })

  it('Should show error with invalid info', () => {
    cy.visit('/login')
    cy.wait(500)
    cy.then(() => {
        cy.get('[data-cy="email-input"]').type('email@invalid.com')
        cy.get('[data-cy="password-input"]').type('pswdwrong')
        cy.get('[data-cy="login-button"]').click()
        cy.contains('Acesse sua conta').should('be.visible')
    })
  })

  it('Should navigate to register page', () => {
    cy.visit('/auth')
    cy.wait(500)
    cy.then(() => {
      cy.get('[data-cy="register-link"]').click()
      cy.url().should('include', '/register')
      cy.contains('Criar conta').should('be.visible')
    })
  })

  it('Should navigate to login page', () => {
    cy.visit('/auth')
    cy.wait(500)
    cy.then(() => {
      cy.get('[data-cy="login-link"]').click()
      cy.url().should('include', '/login')
      cy.contains('Acesse sua conta').should('be.visible')
    })
  })
})