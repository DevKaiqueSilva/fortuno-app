describe('Dashboard', () => {
  beforeEach(() => {
    cy.fixture('user').then((user) => {
      cy.login(user.testUser.email, user.testUser.password)
    })
  })

  it('Should show dashboard labels', () => {
    cy.contains('Contas').should('be.visible')
    cy.contains('Gastos por categoria').should('be.visible')
    cy.contains('Últimas transações').should('be.visible')
  })

  it('Should navigate to wallet menu', () => {
    cy.get('[data-cy="wallets-menu"]').click()
    cy.url().should('include', '/wallet')
    cy.contains('Contas').should('be.visible')
  })

  it('Should navigate to transactions menu', () => {
    cy.get('[data-cy="transactions-menu"]').click()
    cy.url().should('include', '/transactions')
  })

  it('Should navigate to categories menu', () => {
    cy.get('[data-cy="settings-menu"]').click()
    cy.get('[data-cy="categories-menu"]').click()
    cy.url().should('include', '/categories')
    cy.contains('Categorias').should('be.visible')
  })

  it('Should logout', () => {
    cy.get('[data-cy="settings-menu"]').click()
    cy.logout()
    cy.url().should('include', '/login')
  })
})