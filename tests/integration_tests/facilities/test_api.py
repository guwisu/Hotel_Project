


async def test_get_facilities(ac):
    response = await ac.get("/facilities")
    print(f"{response.json()=}")

    assert response.status_code == 200

# async def test_add_facility(ac):
#     response = await ac.post(
#         "/facilities",
#         json={
#             "title": "toilet",
#         }
#     )
#     print(f"{response=}")
#
#     assert response.status_code == 20