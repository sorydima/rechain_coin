/* Public header shim for rechain_core
 * Exposes a stable C API surface to preserve compatibility when refactoring internals.
 */

#ifndef RECHAIN_CORE_H
#define RECHAIN_CORE_H

#ifdef __cplusplus
extern "C" {
#endif

#define RECHAIN_CORE_API_VERSION 1

// Initialize core library. Returns 0 on success.
int rechain_core_init(void);

// Shutdown core library.
void rechain_core_shutdown(void);

#ifdef __cplusplus
}
#endif

#endif // RECHAIN_CORE_H
